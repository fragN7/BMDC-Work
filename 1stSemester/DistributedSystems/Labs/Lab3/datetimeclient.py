import grpc
import datetime
import datetime_pb2
import datetime_pb2_grpc
import threading

def make_request(stub):
    request = datetime_pb2.DateTimeRequest()
    response = stub.GetCurrentDateTime(request)
    return response.datetime
def run():
    with grpc.insecure_channel('localhost:20048') as channel:
        stub = datetime_pb2_grpc.DateTimeStub(channel)

        # create threads to make concurrent requests
        threads = []
        for i in range(5):
            thread = threading.Thread()
            thread.start()
            threads.append(thread)
            print(f"Current date and time: ") 

        # wait for all threads to complete
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    run()
