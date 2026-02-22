import grpc
import time
from concurrent import futures

import example_pb2
import example_pb2_grpc

class ExampleService(example_pb2_grpc.ExampleServiceServicer):
    def GetMessage(self, request, context):
        return example_pb2.Message(text='Hello, {}!'.format(request.name))

    def SendMessage(self, request, context):
        print('Received message: {}'.format(request.text))
        return example_pb2.Result(success=True)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleService(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
