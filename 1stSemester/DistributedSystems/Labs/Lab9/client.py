import grpc
import quorum_pb2
import quorum_pb2_grpc

class QuorumClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:20048')
        self.stub = quorum_pb2_grpc.QuorumStub(self.channel)
    
    def write(self, key, value):
        request = quorum_pb2.Request(key=key, value=value)
        response = self.stub.Write(request)
        return response.success, response.message
    
    def read(self, key):
        request = quorum_pb2.Request(key=key, value="")
        response = self.stub.Read(request)
        return response.success, response.message, response.value

def run_client():
    client = QuorumClient()
    print(client.write("key1", "value1"))
    print(client.read("key1"))
    print(client.read("key2"))

if __name__ == '__main__':
    run_client()
