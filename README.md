# opencensus-for-grpc-python-developers
OpenCensus for gRPC Python developers

## Building it

Install Python3 then use pip3
or
Python3 then use pip

### Dependencies
```shell
pip3 install grpcio-tools
```

### Generate the protobuf definitions
```shell
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./protos/defs.proto
```
