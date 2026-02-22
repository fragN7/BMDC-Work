import concurrent.futures
import grpc
import binary_search_pb2
import binary_search_pb2_grpc

class BinarySearchServicer(binary_search_pb2_grpc.BinarySearchServiceServicer):
    def BinarySearch(self, request, context):
        elements = request.elements
        value = request.value
        left = 0
        right = len(elements) - 1

        while left <= right:
            mid = (left + right) // 2
            if elements[mid] == value:
                return binary_search_pb2.BinarySearchResponse(index=mid)
            elif elements[mid] < value:
                left = mid + 1
            else:
                right = mid - 1

        return binary_search_pb2.BinarySearchResponse(index=-1)

def serve():
    num_threads = int(input("Enter the number of threads to use: "))
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=num_threads))
    binary_search_pb2_grpc.add_BinarySearchServiceServicer_to_server(BinarySearchServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
