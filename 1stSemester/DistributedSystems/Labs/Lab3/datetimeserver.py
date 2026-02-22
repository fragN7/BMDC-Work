from concurrent import futures
import datetime
import grpc
import time

import datetime_pb2
import datetime_pb2_grpc


class DateTimeServicer(datetime_pb2_grpc.DateTimeServicer):
    def GetCurrentDateTime(self, request, context):
        now = datetime.datetime.now().isoformat()
        response = datetime_pb2.DateTimeResponse(datetime=now)
        context.send_initial_metadata([('status', 'success')])
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datetime_pb2_grpc.add_DateTimeServicer_to_server(DateTimeServicer(), server)
    server.add_insecure_port('[::]:20048')
    server.start()
    print("Server started, CONNECTED to port 20048")
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
