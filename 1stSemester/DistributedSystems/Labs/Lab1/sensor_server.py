import grpc
from concurrent import futures

import sensor_pb2
import sensor_pb2_grpc


class SensorService(sensor_pb2_grpc.SensorServiceServicer):

    def SendReadings(self, request_iterator, context):

        values = []

        print("Receiving data...")

        for data in request_iterator:
            print("Received:", data.value)
            values.append(data.value)

        if not values:
            return sensor_pb2.Summary()

        avg = sum(values) / len(values)
        mn = min(values)
        mx = max(values)

        print("Sending summary...")

        return sensor_pb2.Summary(
            average=avg,
            min=mn,
            max=mx
        )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    sensor_pb2_grpc.add_SensorServiceServicer_to_server(
        SensorService(), server
    )

    server.add_insecure_port("[::]:50051")

    server.start()

    print("Server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
