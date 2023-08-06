import typing

from jsonschema import Draft4Validator


class DummyValidator:
    @staticmethod
    def is_valid(data: dict):
        return True


class Parameters:
    def __init__(self, params: dict = None, files: typing.Dict[str, bytes] = None):
        if not params:
            params = dict()
        if not files:
            files = dict()

        self.params = params
        self.files = files

    def __repr__(self):
        return f"Parameters(params={self.params}, files={list(self.files.keys())})"


class Procedure:
    def __init__(self, function, scheme=None):
        self.function = function

        self.scheme = scheme if scheme else dict()
        self.validator = Draft4Validator(self.scheme)

    def is_valid(self, data: Parameters) -> bool:
        return self.validator.is_valid(data.params)

    def call_function(self, data: Parameters) -> Parameters:
        return Parameters(*self.function(data.params, data.files))

    def __call__(self, data: Parameters) -> Parameters:
        return self.call_function(data)
