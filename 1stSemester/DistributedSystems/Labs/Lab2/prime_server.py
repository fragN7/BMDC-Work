import grpc
from concurrent import futures
import math

import prime_pb2
import prime_pb2_grpc


def is_prime(n):

    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    return True


class PrimeService(prime_pb2_grpc.PrimeServiceServicer):

    def CheckPrime(self, request, context):

        number = request.number

        result = is_prime(number)

        print(f"Checking {number} → {result}")

        return prime_pb2.PrimeResponse(
            number=number,
            is_prime=result
        )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    prime_pb2_grpc.add_PrimeServiceServicer_to_server(
        PrimeService(), server
    )

    server.add_insecure_port("[::]:50052")

    server.start()

    print("Prime server running on port 50052")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
