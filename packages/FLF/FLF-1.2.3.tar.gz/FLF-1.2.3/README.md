# FLF

RabbitMQ server and client

## Installation

To install execute command:

```bash
pip install FLF==1.1.0 --ignore-installed
```

Or you can install from source:

```bash
python setup.py install
````

## Documentation

### RpcServer

Server-node for RabbitMQ

Parameters:

* **host**: host of queue
* **port**: port of queue
* **username**: username of queue
* **password**: password of queue
* **procedures**: dictionary with server's procedures in format: `{ str: FLF.Parameters }`. 
Each procedure has fields `params` (dict of parameters) and `files` (dict of binary objects) and 
returns data in same format (`FLF.Parameters(params, files)`)
* **error_callback**: callable with `3` arguments: `exception_name`, `description` and `traceback`. 
Being called on error happening

Example:

```python
import io

from PIL import Image

import FLF


def add(params, files):
    result_params = {"success": True, "sum": params["a"] + params["b"]}
    result_files = dict()
    
    return result_params, result_files


def get_add_schema():
    return {
        "$schema": "http://json-schema.org/draft-04/schema",
        "id": "http://example.com/example.json",
        "type": "object",
        "required": [
            "a",
            "b"
        ],
        "properties": {
            "a": {
                "type": "integer"
            },
            "b": {
                "type": "integer"
            }
        },
        "additionalProperties": False
    }


def process_image(params, files):
    pil_image = Image.frombuffer("RGB", (params["width"], params["height"]), files["image"])
    image_gray = pil_image.convert("LA")
    
    buffer = io.BytesIO()
    image_gray.save(buffer, format='PNG')
    image_gray_bytes = buffer.getvalue()
    
    return {"success": True}, {"gray_image": image_gray_bytes}


def get_process_image_schema():
    return {
        "$schema": "http://json-schema.org/draft-04/schema",
        "id": "http://example.com/example.json",
        "type": "object",
        "required": [
            "width",
            "height"
        ],
        "properties": {
            "width": {
                "type": "integer"
            },
            "height": {
                "type": "integer"
            }
        },
        "additionalProperties": False
    }


def super_error_callback(exception_name, description, traceback):
    print("OH MY GOD, SOMETHING BAD HAPPENED!")
    print(exception_name, ":", description)
    print(traceback)


def main():
    app = FLF.RpcServer(host="google.com", port=12345, username="mister.robot", password="ecorp.zuck",
                        procedures={
                            "add": FLF.Procedure(add, get_add_schema()),
                            "process_image": FLF.Procedure(process_image, get_process_image_schema())
                        }, error_callback=super_error_callback)
    app.begin()


if __name__ == "__main__":
    main()

```

### RpcConnector

Client-node for RabbitMQ

Parameters:

* **host**: host of queue
* **port**: port of queue
* **username**: username of queue
* **password**: password of queue
* **error_callback**: callable with `3` arguments: `exception_name`, `description` and `traceback`. 
Being called on error happening

Example:

```python
import FLF


def super_error_callback(exception_name, description, traceback):
    print("OH MY GOD, SOMETHING BAD HAPPENED ON CLIENT!")
    print(exception_name, ":", description)
    print(traceback)


def main():
    app = FLF.RpcConnector(host="google.com", port=12345, username="mister.robot", password="ecorp.zuck",
                           error_callback=super_error_callback)
    app.begin()
    
    params, _ = app.call_procedure("add", FLF.Parameters({"a": 22, "b": 33}))
    print("Sum is:", params["sum"])
    
    with open("image.jpg", "rb") as f:
        image_bytes = f.read()
    result: FLF.Parameters = app.call_procedure("process_image", FLF.Parameters({"width": 500, "height": 500},
                                                                    {"image": image_bytes}))
    
    with open("image_gray.png", "wb+") as f:
        f.write(result.files["gray_image"])


if __name__ == "__main__":
    main()

```
