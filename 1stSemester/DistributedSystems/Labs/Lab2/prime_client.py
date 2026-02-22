import grpc
import threading
import random

import prime_pb2
import prime_pb2_grpc


SERVER = "localhost:50052"


def worker(thread_id, numbers):

    channel = grpc.insecure_channel(SERVER)
    stub = prime_pb2_grpc.PrimeServiceStub(channel)

    for num in numbers:

        response = stub.CheckPrime(
            prime_pb2.PrimeRequest(number=num)
        )

        print(
            f"[Thread {thread_id}] "
            f"{response.number} → "
            f"{response.is_prime}"
        )


def main():

    numbers = [
        random.randint(100000, 200000)
        for _ in range(40)
    ]

    threads = []

    NUM_THREADS = 5

    chunk_size = len(numbers) // NUM_THREADS


    for i in range(NUM_THREADS):

        start = i * chunk_size
        end = start + chunk_size

        part = numbers[start:end]

        t = threading.Thread(
            target=worker,
            args=(i + 1, part)
        )

        threads.append(t)
        t.start()


    for t in threads:
        t.join()

    print("\nAll threads finished.")


if __name__ == "__main__":
    main()
