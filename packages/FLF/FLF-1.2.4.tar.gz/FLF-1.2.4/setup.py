from setuptools import setup
from distutils.util import convert_path


version_dict = {}
version_path = convert_path('FLF/version.py')
with open(version_path) as version_file:
    exec(version_file.read(), version_dict)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="FLF",
    packages=["FLF"],
    version=version_dict["__version__"],
    license="MIT",
    description="Server and Connector for RabbitMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DenisVASI9, evjeny",
    author_email="gkanafing@gmail.com",
    url="https://github.com/DenisVASI9/FLF",
    keywords=["RabbitMQ", "RPCServer", "RPCConnector", "pika"],
    install_requires=[
        "pika", 'jsonschema'
    ],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6"
    ]
)
