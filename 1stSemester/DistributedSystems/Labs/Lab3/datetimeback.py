import datetime
import grpc
import random
import time

import datetime_pb2
import datetime_pb2_grpc


def get_current_datetime(stub):
    request = datetime_pb2.DateTimeRequest()
    response = stub.GetCurrentDateTime(request)
    return response.datetime


def run():
    while True:
        try:
            with grpc.insecure_channel('localhost:20048') as channel:
                stub = datetime_pb2_grpc.DateTimeStub(channel)
                for i in range(7):
                    print(f"Retry {i+1}")
                    datetime = get_current_datetime(stub)
                    print(f"Current date and time: {datetime}")
                    time.sleep(random.uniform(0, 2 ** i))  # Backoff exponentially
                break  # Break out of loop if successful
        except grpc.RpcError as e:
            print(f"Error: {e}")
            time.sleep(1)  # Wait for a second before retrying


if __name__ == '__main__':
    run()
