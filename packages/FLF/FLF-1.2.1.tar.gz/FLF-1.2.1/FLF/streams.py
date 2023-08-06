from enum import Enum
import json
import typing
import uuid

import pika

from FLF.procedure import Parameters


class RequestType(Enum):
    INPUT = "input"
    OUTPUT = "output"


def make_request_headers(size: int, mask: int, batch_name: str, request_id: str, address_type: str,
                         address_value: str) -> typing.Dict:
    headers = {
        "request_size": size,
        "request_mask": mask,
        "batch_name": batch_name,
        "req_id": request_id,
        address_type: address_value
    }
    return headers


def publish_response(request_type: RequestType, channel, req_id: str, reply_to: str, correlation_id: str,
                     response_value: str, data: Parameters):
    params = data.params
    files = data.files

    size = 1 + len(files)

    # make params headers
    addr_type = "response_id" if request_type == RequestType.INPUT else "call_procedure"

    params_mask = 1
    params_headers = make_request_headers(size, params_mask, "params", req_id, addr_type, response_value)
    additional_info = dict() if request_type == RequestType.INPUT else {"reply_to": reply_to}
    params_properties = pika.BasicProperties(correlation_id=correlation_id, headers=params_headers, **additional_info)
    routing_key = reply_to if request_type == RequestType.INPUT else "rpc_queue"

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
    def __init__(self, channel, correlation_id: str, reply_to: str, data: Parameters):
        self.data = data

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, response_id: str) -> None:
        req_id = str(uuid.uuid4())
        publish_response(RequestType.INPUT, self.channel, req_id, self.reply_to, self.correlation_id, response_id,
                         self.data)


class OutputStream:
    def __init__(self, channel, correlation_id: str, reply_to: str, data: Parameters):
        self.data = data

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, name: str, req_id: str) -> None:
        publish_response(RequestType.OUTPUT, self.channel, req_id, self.reply_to, self.correlation_id, name, self.data)
