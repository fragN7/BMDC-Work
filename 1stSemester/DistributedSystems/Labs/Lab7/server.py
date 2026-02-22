import grpc
from concurrent import futures
import time
import ring_pb2
import ring_pb2_grpc

class RingElectionServicer(ring_pb2_grpc.RingElectionServicer):
    def StartElection(self, request, context):
        print(f"Received election message from process {request.sender_id} with election ID {request.election_id}")
        if request.sender_id == 3:
            print("I am process 3 and I am initiating the election")
            result = ring_pb2.ElectionResult()
            result.leader_id = 3
            result.success = True
            return result
        else:
            print(f"Forwarding election message from process {request.sender_id} to process {request.sender_id+1}")
            with grpc.insecure_channel(f'localhost:{request.sender_id+1}') as channel:
                stub = ring_pb2_grpc.RingElectionStub(channel)
                response = stub.StartElection(ring_pb2.ElectionMessage(sender_id=request.sender_id+1, election_id=request.election_id))
                return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ring_pb2_grpc.add_RingElectionServicer_to_server(RingElectionServicer(), server)
    server.add_insecure_port('[::]:20048')
    server.start()
    print("Server started listening on DESIGNATED port")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
