import grpc
from concurrent import futures
import random
import time

import quorum_pb2
import quorum_pb2_grpc

class Replica(quorum_pb2_grpc.QuorumServicer):
    def __init__(self, id):
        self.id = id
        self.data = {}
    
    def Write(self, request, context):
        self.data[request.key] = request.value
        return quorum_pb2.Response(success=True, message="Write succeeded", value="")
    
    def Read(self, request, context):
        if request.key in self.data:
            return quorum_pb2.Response(success=True, message="Read succeeded", value=self.data[request.key])
        else:
            return quorum_pb2.Response(success=False, message="Read failed", value="")

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    quorum_pb2_grpc.add_QuorumServicer_to_server(Replica(1), server)
    quorum_pb2_grpc.add_QuorumServicer_to_server(Replica(2), server)
    quorum_pb2_grpc.add_QuorumServicer_to_server(Replica(3), server)
    quorum_pb2_grpc.add_QuorumServicer_to_server(Replica(4), server)
    quorum_pb2_grpc.add_QuorumServicer_to_server(Replica(5), server)
    server.add_insecure_port('[::]:20048')
    server.start()

    print('Starting server. Ready for Quorum check!.')

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run_server()
