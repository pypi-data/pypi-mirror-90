import json
import typing

from FLF.procedure import Parameters


class Store:
    def __init__(self, callback: typing.Callable[[Parameters, str, str, str, str], None]):
        self.store = dict()
        self.callback = callback

    def add(self, key: str, name: str, value: bytes, size: int, mask: int, procedure_name: str, reply_to: str,
            req_id: str):
        if req_id not in self.store:
            self.store[req_id] = {"params": {}, "files": {}, "mask": 0}
        self.store[req_id]["mask"] |= mask

        if name == "params":
            self.store[req_id]["params"] = json.loads(value.decode("utf-8"))
        else:
            self.store[req_id]["files"][name] = value

        full_mask = (1 << size) - 1
        if self.store[req_id]["mask"] == full_mask:
            result = self.store.pop(req_id)
            result = Parameters(result["params"], result["files"])
            self.on_request_complete(result, key, procedure_name, reply_to, req_id)

    def on_request_complete(self, data: Parameters, key: str, procedure_name: str, reply_to: str, req_id: str):
        self.callback(data, key, procedure_name, reply_to, req_id)
