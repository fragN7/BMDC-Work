import grpc

import example_pb2
import example_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = example_pb2_grpc.ExampleServiceStub(channel)

response = stub.GetMessage(example_pb2.Name(name='Distributed Class'))
print(response.text)

send_response = stub.SendMessage(example_pb2.Message(text='Hello from the client!'))
print('Send message result: {}'.format(send_response.success))
