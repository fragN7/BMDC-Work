import grpc
import binary_search_pb2
import binary_search_pb2_grpc
import sys

def run():
    elements_str = sys.argv[1]
    elements = [int(e) for e in elements_str.split(',')]
    value = int(input("Enter the value to search: "))
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = binary_search_pb2_grpc.BinarySearchServiceStub(channel)
        response = stub.BinarySearch(binary_search_pb2.BinarySearchRequest(elements=elements, value=value))
    print("Index of value {}: {}".format(value, response.index))

if __name__ == '__main__':
    run()
