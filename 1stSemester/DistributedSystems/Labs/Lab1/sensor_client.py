import grpc
import time

import sensor_pb2
import sensor_pb2_grpc


def generate_data():

    values = [20.1, 20.5, 21.0, 19.8, 22.2]

    for v in values:
        print("Sending:", v)

        yield sensor_pb2.SensorData(value=v)

        time.sleep(1)


def run():

    channel = grpc.insecure_channel("localhost:50051")

    stub = sensor_pb2_grpc.SensorServiceStub(channel)

    print("Sending sensor data...\n")

    response = stub.SendReadings(generate_data())

    print("\nSummary received:")
    print("Average:", response.average)
    print("Min:", response.min)
    print("Max:", response.max)


if __name__ == "__main__":
    run()
