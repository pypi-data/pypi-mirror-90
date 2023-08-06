import json
import traceback
import uuid

import pika
from pika.exceptions import AMQPConnectionError, ProbableAuthenticationError

from FLF.exceptions import ProcedureExecutionException


class Store:
    def __init__(self, callback):
        self.store = {}
        self.callback = callback

    def add(self, key, name, value, size, mask, call_procedure, reply_to, req_id):
        if req_id not in self.store:
            self.store[req_id] = {"params": {}, "files": {}, "mask": 0}
        self.store[req_id]["mask"] |= mask

        if name == "params":
            self.store[req_id]["params"] = json.loads(value.decode("utf-8"))
        else:
            self.store[req_id]["files"][name] = value

        if self.store[req_id]["mask"] == (2 ** size - 1):
            result = self.store.pop(req_id)
            result.pop("mask")
            self.on_request_complete(result, key, call_procedure, reply_to, req_id)

    def on_request_complete(self, data, key, call_procedure, reply_to, req_id):
        self.callback(data, key, call_procedure, reply_to, req_id)


def make_request_headers(size, mask, batch_name, request_id, address_type, address_value):
    headers = {
        "request_size": size,
        "request_mask": mask,
        "batch_name": batch_name,
        "req_id": request_id,
        address_type: address_value
    }
    return headers


def publish_response(response_type, channel, req_id, reply_to, correlation_id, response_value, params, files):
    size = (1 if len(params) else 0) + len(files)

    # make params headers
    addr_type = "response_id" if response_type == "input" else "call_procedure"

    params_mask = 1 if len(params) else 0
    params_headers = make_request_headers(size, params_mask, "params", req_id, addr_type, response_value)
    additional_info = dict() if response_type == "input" else {"reply_to": reply_to}
    params_properties = pika.BasicProperties(correlation_id=correlation_id, headers=params_headers, **additional_info)
    routing_key = reply_to if response_type == "input" else "rpc_queue"

    # send params
    channel.basic_publish(exchange="", properties=params_properties, body=json.dumps(params), routing_key=routing_key)

    for i, (file_name, file_content) in enumerate(files.items()):
        # make file headers
        file_mask = 1 << (1 + i)
        file_headers = make_request_headers(size, file_mask, file_name, req_id, addr_type, response_value)
        file_properties = pika.BasicProperties(correlation_id=correlation_id, headers=file_headers, **additional_info)

        # send file
        channel.basic_publish(exchange="", properties=file_properties, body=file_content, routing_key=routing_key)


class InputStream:
    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):
        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, response_id):
        req_id = str(uuid.uuid4())
        publish_response("input", self.channel, req_id, self.reply_to, self.correlation_id, response_id,
                         self.params, self.files)


class OutputStream:
    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):
        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, name, req_id):
        publish_response("output", self.channel, req_id, self.reply_to, self.correlation_id, name,
                         self.params, self.files)


def create_connection(host, port, username, password):
    credentials = pika.PlainCredentials(username=username, password=password)
    connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)

    return connection


class RpcServer:
    def __init__(self, host, port, username, password, procedures=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        if procedures is None:
            procedures = dict()

        self.procedures = procedures
        self.connection = None
        self.channel = None
        self.store = Store(self.on_complete_callback)

    def on_message(self, channel, method, props, body):
        request_size = props.headers["request_size"]
        request_mask = props.headers["request_mask"]
        batch_name = props.headers["batch_name"]
        correlation_id = props.correlation_id
        reply_to = props.reply_to
        call_procedure = props.headers["call_procedure"]
        req_id = props.headers["req_id"]

        # if server has needed procedure
        if call_procedure in self.procedures:
            self.on_request(request_size, request_mask, batch_name, correlation_id, reply_to,
                            call_procedure, body, req_id)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)

    def on_complete_callback(self, data, key, call_procedure, reply_to, req_id):
        try:
            result_params, result_files = self.procedures[call_procedure](data["params"], data["files"])
            response = InputStream(self.channel, key, reply_to, result_params, result_files)
            response.send(req_id)
        except Exception as e:
            body = {"exception": str(e),
                    "description": f"Failed to execute procedure '{call_procedure}'",
                    "traceback": traceback.format_exc()}
            response = InputStream(self.channel, key, reply_to, body)
            response.send(req_id)

    # код приема запроса
    def on_request(self, size, mask, batch_name, correlation_id, reply_to, call_procedure, body, req_id):
        self.store.add(correlation_id, batch_name, body, size, mask, call_procedure, reply_to, req_id)

    def connect(self):
        print("Rpc server connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError as e:
            raise RuntimeError(f"Authorization error, code 1: {str(e)}")
        except AMQPConnectionError as e:
            raise RuntimeError(f"Connection error, code 2: {str(e)}")

    def create_req_channel(self, connection):
        print("Rpc server creates a channel")

        channel = connection.channel()
        channel.queue_declare(queue="rpc_queue")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="rpc_queue", on_message_callback=self.on_message)
        self.channel = channel

    def listen(self):
        print("Listening")
        self.channel.start_consuming()

    def begin(self):
        while True:
            try:
                with self.connect() as connection:
                    self.create_req_channel(connection)
                    self.listen()
            except Exception as e:
                print("Exception:", str(e))


class RpcConnector:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.store = Store(self.on_complete_callback)

    def on_message(self, channel, method, props, body):
        correlation_id = props.correlation_id
        request_size = props.headers["request_size"]
        request_mask = props.headers["request_mask"]
        batch_name = props.headers["batch_name"]
        req_id = props.headers["req_id"]

        if self.correlation_id == correlation_id:
            self.on_response(request_size, request_mask, batch_name, correlation_id, body, req_id)

    def on_complete_callback(self, data, key, call_procedure, reply_to, req_id):
        self.response = data

    def on_response(self, size, mask, batch_name, correlation_id, body, req_id):
        self.store.add(correlation_id, batch_name, body, size, mask, None, None, req_id)

    def call_procedure(self, name, params=None, files=None):
        try:
            self.response = None

            if params is None:
                params = dict()
            if files is None:
                files = dict()

            req_id = str(uuid.uuid4())

            request = OutputStream(self.channel, self.correlation_id, self.callback_queue, params, files)
            request.send(name, req_id)

            while not self.response:
                self.connection.process_data_events()

            return self.response["params"], self.response["files"]
        except Exception as e:
            raise ProcedureExecutionException(f"Failed to execute procedure '{name}': {str(e)}\n" +
                                              "{traceback.format_exc()}")

    def connect(self):
        print("Rpc client connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError as e:
            raise RuntimeError(f"Authorization error, code 1: {str(e)}")
        except AMQPConnectionError as e:
            raise RuntimeError(f"Connection error, code 2: {str(e)}")

    def create_channel(self):
        print("Rpc client creates the channel")

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_message, auto_ack=True)

    def begin(self):
        self.connection = self.connect()
        self.create_channel()

