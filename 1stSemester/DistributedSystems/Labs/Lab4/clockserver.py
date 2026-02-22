import datetime
import grpc
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import datetime_pb2
import datetime_pb2_grpc

class DateTimeServicer(datetime_pb2_grpc.DateTimeServiceServicer):
    def GetDateTime(self, request, context):
        current_time = datetime.datetime.utcnow()
        response = datetime_pb2.DateTimeResponse()
        response.date_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
        return response

def run_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port("[::]:20048")
    datetime_pb2_grpc.add_DateTimeServiceServicer_to_server(DateTimeServicer(), server)
    server.start()
    print("Server CONNECTED to port 20048...")
    server.wait_for_termination()

if __name__ == "__main__":
    run_server()
