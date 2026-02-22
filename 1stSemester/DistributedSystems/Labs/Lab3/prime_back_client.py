# client_with_backoff.py

import grpc
import prime_pb2
import prime_pb2_grpc
import time
from datetime import datetime

SERVER = "localhost:50052"
MAX_RETRIES = 5
BASE_DELAY = 1  # seconds

def call_with_backoff(stub, number):
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            response = stub.CheckPrime(prime_pb2.PrimeRequest(number=number))
            print(f"{datetime.now()} → {number} → {response.is_prime}")
            return response
        except grpc.RpcError as e:
            print(f"{datetime.now()} → Attempt {attempt+1} failed for {number}: {e}")
            delay = BASE_DELAY * (2 ** attempt)
            print(f"Waiting {delay} seconds before retry...")
            time.sleep(delay)
            attempt += 1

    print(f"{datetime.now()} → Failed to get response for {number} after {MAX_RETRIES} attempts")
    return None


def main():
    numbers = [17, 18, 19, 20, 21]
    channel = grpc.insecure_channel(SERVER)
    stub = prime_pb2_grpc.PrimeServiceStub(channel)

    for n in numbers:
        call_with_backoff(stub, n)


if __name__ == "__main__":
    main()
