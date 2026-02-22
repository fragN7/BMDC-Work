import grpc
from concurrent import futures
import threading
import time
import random
from queue import Queue
import lamportclock_pb2_grpc
import lamportclock_pb2

class ResourceServer(lamportclock_pb2_grpc.LamportClockServicer):
    def __init__(self):
        self.clock = 0
        self.queue = Queue()
        self.granted = False

    def Request(self, request, context):
        print(f"Received request from {request.process_id} at time {request.timestamp}")
        self.clock = max(self.clock, request.timestamp) + 1
        if not self.granted:
            print(f"Granting resource to {request.process_id}")
            self.granted = True
            return lamportclock_pb2.ResourceReply(granted=True)
        else:
            print(f"Resource busy, adding {request.process_id} to queue")
            self.queue.put(request)
            waiting = []
            while not self.queue.empty():
                waiting.append(self.queue.get())
            return lamportclock_pb2.ResourceReply(granted=False, waiting=waiting)

    def Release(self, request, context):
        print(f"Received release from {request.process_id} at time {request.timestamp}")
        self.clock = max(self.clock, request.timestamp) + 1
        if not self.queue.empty():
            next_request = self.queue.get()
            print(f"Granting resource to {next_request.process_id}")
            return lamportclock_pb2.Empty()
        else:
            print("Resource released, no pending requests")
            self.granted = False
            return lamportclock_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lamportclock_pb2_grpc.add_LamportClockServicer_to_server(ResourceServer(), server)
    server.add_insecure_port('[::]:20048')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
