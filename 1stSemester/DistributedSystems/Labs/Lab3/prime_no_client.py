# client_no_backoff.py

import grpc
import prime_pb2
import prime_pb2_grpc

SERVER = "localhost:50052"

def simple_client(numbers):
    channel = grpc.insecure_channel(SERVER)
    stub = prime_pb2_grpc.PrimeServiceStub(channel)

    for n in numbers:
        try:
            response = stub.CheckPrime(prime_pb2.PrimeRequest(number=n))
            print(f"{n} → {response.is_prime}")
        except grpc.RpcError as e:
            print(f"Failed to call server for {n}: {e}")


if __name__ == "__main__":
    numbers = [17, 18, 19, 20, 21]
    simple_client(numbers)
