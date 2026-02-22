import grpc
import ring_pb2
import ring_pb2_grpc

def initiate_election():
    with grpc.insecure_channel('localhost:20048') as channel:
        stub = ring_pb2_grpc.RingElectionStub(channel)
        response = stub.StartElection(ring_pb2.ElectionMessage(sender_id=3, election_id=1))
        if response.success:
            print(f"Election completed successfully. Coordinator ID is {response.leader_id}")
        else:
            print("Election failed")

if __name__ == '__main__':
    initiate_election()
