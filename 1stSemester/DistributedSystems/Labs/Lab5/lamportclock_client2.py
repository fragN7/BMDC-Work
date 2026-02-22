import grpc
import threading
import time
import random
import lamportclock_pb2_grpc
import lamportclock_pb2


class ResourceClient:
    def __init__(self, process_id):
        self.process_id = process_id
        self.channel = grpc.insecure_channel('localhost:20048')
        self.stub = lamportclock_pb2_grpc.LamportClockStub(self.channel)
        self.clock = 0
        self.granted = False

    def send_request(self):
        self.clock += 1
        request = lamportclock_pb2.ResourceRequest(process_id=self.process_id, timestamp=self.clock)
        response = self.stub.Request(request)
        self.clock = max(self.clock, self.get_max_timestamp(response.waiting)) + 1
        if response.granted:
            print(f"{self.process_id} granted resource at time {self.clock}")
            self.granted = True
        else:
            print(f"{self.process_id} waiting for resource at time {self.clock}")
            self.granted = False
            threading.Timer(1.0, self.send_request).start()

    def send_release(self):
        if self.granted:
            self.clock += 1
            request = lamportclock_pb2.ResourceRelease(process_id=self.process_id, timestamp=self.clock)
            self.stub.Release(request)
            self.granted = False
            print(f"{self.process_id} released resource at time {self.clock}")
        else:
            print(f"{self.process_id} has not been granted the resource yet at time {self.clock}")

    def get_max_timestamp(self, requests):
        max_timestamp = self.clock
        for request in requests:
            max_timestamp = max(max_timestamp, request.timestamp)
        return max_timestamp

if __name__ == '__main__':
    client_a = ResourceClient('Process A')
    client_b = ResourceClient('Process B')
    client_c = ResourceClient('Process C')
    client_d = ResourceClient('Process D')

    # start process A with the resource initially granted
    client_a.granted = True
    client_a.send_request()

    # start processes B, C, and D
    threading.Timer(random.randint(1, 5), client_b.send_request).start()
    threading.Timer(random.randint(1, 5), client_c.send_request).start()
    threading.Timer(random.randint(1, 5), client_d.send_request).start()

    # periodically release the resource for each process
    while True:
        time.sleep(10)
        client_a.send_release()
        client_b.send_release()
        client_c.send_release()
        client_d.send_release()
        print(f"Resource usage: A: {client_a.granted}, B: {client_b.granted}, C: {client_c.granted}, D: {client_d.granted}")
