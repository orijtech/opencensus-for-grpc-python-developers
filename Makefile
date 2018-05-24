all: gen_protoc deps

gen_protoc:
	python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/defs.proto

deps:
	pip3 install grpcio-tools
