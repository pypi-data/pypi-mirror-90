import traceback
import typing
import uuid

import pika
from pika.exceptions import AMQPConnectionError, ProbableAuthenticationError

from FLF.store import Store
from FLF.streams import InputStream, OutputStream
from FLF.procedure import Procedure, Parameters
from FLF.exceptions import ProcedureExecutionException, InvalidDataException


def create_connection(host: str, port: int, username: str, password: str) -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(username=username, password=password)
    connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)

    return connection


def default_error_callback(exception_name, description, tb):
    pass


class RpcServer:
    def __init__(self, host: str, port: int, username: str, password: str,
                 procedures: typing.Dict[str, Procedure], greedy: bool = True,
                 error_callback: typing.Callable[[str, str, str], None] = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.greedy = greedy
        self.procedures = procedures

        if error_callback:
            self.error_callback = error_callback
        else:
            self.error_callback = default_error_callback

        self.connection = None
        self.channel = None
        self.store = Store(self.on_complete_callback)

    def on_message(self, channel, method, props, body: bytes) -> None:
        try:
            request_size = props.headers["request_size"]
            request_mask = props.headers["request_mask"]
            batch_name = props.headers["batch_name"]
            correlation_id = props.correlation_id
            reply_to = props.reply_to
            call_procedure = props.headers["call_procedure"]
            req_id = props.headers["req_id"]
        except KeyError as e:
            self.error_callback("KeyError", f"Can't find key: {str(e)}", traceback.format_exc())

            if self.greedy:                
                self.channel.basic_ack(delivery_tag=method.delivery_tag)

                body = b'{"success": false}'
                self.on_request(1, 1, "hello_world", correlation_id, reply_to, "", body, "")
            else:
                self.channel.basic_nack(delivery_tag=method.delivery_tag)

            return

        # if server has needed procedure
        if call_procedure in self.procedures:
            self.on_request(request_size, request_mask, batch_name, correlation_id, reply_to,
                            call_procedure, body, req_id)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)

    def on_complete_callback(self, data: Parameters, key: str, procedure_name: str, reply_to: str, req_id: str) -> None:
        try:
            if not self.procedures[procedure_name].is_valid(data):
                raise InvalidDataException("Data doesn't fit the scheme!")

            result = self.procedures[procedure_name](data)
        except InvalidDataException as e:
            self.error_callback("InvalidDataException", str(e), "")

            body = {"exception": "InvalidDataException",
                    "scheme": self.procedures[procedure_name].scheme,
                    "description": str(e),
                    "success": False}
            result = Parameters(body)
        except Exception as e:
            self.error_callback("ProcedureExecutionException", str(e), traceback.format_exc())
            body = {"exception": "ProcedureExecutionException",
                    "description": f"Failed to execute procedure '{procedure_name}': {str(e)}",
                    "traceback": traceback.format_exc(),
                    "success": False}
            result = Parameters(body)

        response = InputStream(self.channel, key, reply_to, result)
        response.send(req_id)

    def on_request(self, size: int, mask: int, batch_name: str, correlation_id: str, reply_to: str, call_procedure: str,
                   body: bytes, req_id: str) -> None:
        self.store.add(correlation_id, batch_name, body, size, mask, call_procedure, reply_to, req_id)

    def connect(self) -> pika.BlockingConnection:
        print("Rpc server connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError as e:
            self.error_callback("ProbableAuthenticationError", str(e), "")
            raise e
        except AMQPConnectionError as e:
            self.error_callback("AMQPConnectionError", str(e), "")
            raise e

    def create_req_channel(self, connection: pika.BlockingConnection) -> None:
        print("Rpc server creates a channel")

        channel = connection.channel()
        channel.queue_declare(queue="rpc_queue")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="rpc_queue", on_message_callback=self.on_message)
        self.channel = channel

    def listen(self) -> None:
        print("Listening")
        self.channel.start_consuming()

    def begin(self) -> None:
        while True:
            try:
                with self.connect() as connection:
                    self.create_req_channel(connection)
                    self.listen()
            except Exception as e:
                self.error_callback("RuntimeException", str(e), traceback.format_exc())
                print("Exception:", str(e))


class RpcConnector:
    def __init__(self, host: str, port: int, username: str, password: str,
                 error_callback: typing.Callable[[str, str, str], None] = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        if error_callback:
            self.error_callback = error_callback
        else:
            self.error_callback = default_error_callback

        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.store = Store(self.on_complete_callback)

    def on_message(self, channel, method, props, body: bytes):
        correlation_id = props.correlation_id
        request_size = props.headers["request_size"]
        request_mask = props.headers["request_mask"]
        batch_name = props.headers["batch_name"]
        req_id = props.headers["req_id"]

        if self.correlation_id == correlation_id:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.on_response(request_size, request_mask, batch_name, correlation_id, body, req_id)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)

    def on_complete_callback(self, data: Parameters, key: str, call_procedure: str, reply_to: str, req_id: str):
        self.response = data

    def on_response(self, size: int, mask: int, batch_name: str, correlation_id: str, body: bytes, req_id: str):
        self.store.add(correlation_id, batch_name, body, size, mask, None, None, req_id)

    def call_procedure(self, name: str, data: Parameters) -> Parameters:
        try:
            self.response = None
            req_id = str(uuid.uuid4())

            request = OutputStream(self.channel, self.correlation_id, self.callback_queue, data)
            request.send(name, req_id)

            while not self.response:
                self.connection.process_data_events()

            return self.response
        except Exception as e:
            self.error_callback("ProcedureExecutionException", str(e), traceback.format_exc())
            raise ProcedureExecutionException(f"Failed to execute procedure '{name}': {str(e)}\n" +
                                              f"{traceback.format_exc()}")

    def connect(self) -> pika.BlockingConnection:
        print("Rpc client connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError as e:
            self.error_callback("ProbableAuthenticationError", str(e), "")
            raise e
        except AMQPConnectionError as e:
            self.error_callback("AMQPConnectionError", str(e), "")
            raise e

    def create_channel(self):
        print("Rpc client creates the channel")

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_message)

    def begin(self) -> None:
        self.connection = self.connect()
        self.create_channel()
