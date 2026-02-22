import grpc
import threading
import time
import datetime

import datetime_pb2
import datetime_pb2_grpc

class DateTimeClient:
    def __init__(self, channel):
        self.stub = datetime_pb2_grpc.DateTimeServiceStub(channel)

    def get_datetime(self):
        request = datetime_pb2.DateTimeRequest()
        response = self.stub.GetDateTime(request)
        return response.date_time

def run_client():
    with grpc.insecure_channel("localhost:20048") as channel:
        client = DateTimeClient(channel)

        # Cristian's algorithm implemetatation
        start_time = time.time()
        server_time = datetime.datetime.strptime(client.get_datetime(), "%Y-%m-%d %H:%M:%S.%fZ")
        end_time = time.time()

        client_time = datetime.datetime.utcnow()
        estimated_server_time = server_time + datetime.timedelta(seconds=(end_time - start_time) / 2)
        time_diff = estimated_server_time - client_time

        print("Client time: ", client_time)
        print("Estimated server time: ", estimated_server_time)
        print("Corrected time: ", time_diff)

if __name__ == "__main__":
    run_client()
