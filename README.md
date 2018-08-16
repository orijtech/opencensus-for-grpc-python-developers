# opencensus-for-grpc-python-developers
OpenCensus for gRPC Python developers

## Building it

Install `Python3` then use `pip3`
or
`Python2` then use `pip`

### Dependencies

With Python2
```shell
pip3 install grpcio-tools opencensus google-cloud-trace
```

OR

With Python2
```shell
pip install grpcio-tools opencensus google-cloud-trace
````

### Generate the protobuf definitions
```shell
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./protos/defs.proto
```
