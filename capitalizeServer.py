#!/usr/bin/env python3

# Copyright 2018, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc
import os
import time
from concurrent import futures

import defs_pb2_grpc as proto
import defs_pb2 as pb

# Tracing related imports
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace.exporters.transports.background_thread import BackgroundThreadTransport
from opencensus.trace.samplers import always_on
from opencensus.trace.tracer import Tracer
from opencensus.trace.ext.grpc import server_interceptor

# Create the exporters:
# 1. Stackdriver
stackdriverExporter = stackdriver_exporter.StackdriverExporter(
            project_id=os.environ.get('OCGRPC_PROJECTID', 'census-demos'),
            transport=BackgroundThreadTransport)

class CapitalizeServer(proto.FetchServicer):
    def __init__(self, *args, **kwargs):
        super(CapitalizeServer, self).__init__()

    def Capitalize(self, request, context):
        tracer = Tracer(sampler=always_on.AlwaysOnSampler(), exporter=stackdriverExporter)
        with tracer.span(name='Capitalize') as span:
            data = request.data
            span.add_annotation('Data in', len=len(data))
            return pb.Payload(data=data.upper())

def main():
    # Setup and start the gRPC server with the OpenCensus integration/interceptor
    tracer_interceptor = server_interceptor.OpenCensusServerInterceptor(
            always_on.AlwaysOnSampler(), stackdriverExporter)

    server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            interceptors=(tracer_interceptor,))
    proto.add_FetchServicer_to_server(CapitalizeServer(), server)
    server.add_insecure_port('[::]:9778')
    server.start()

    try:
        while True:
            time.sleep(60 * 60)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()
