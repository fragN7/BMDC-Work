import grpc
from concurrent import futures
import uuid
import threading

import disttag_pb2
import disttag_pb2_grpc


class GameMaster(disttag_pb2_grpc.GameMasterServicer):

    def __init__(self):
        self.players = {}
        self.it_player = None
        self.lock = threading.Lock()

        self.regions = [
            "localhost:6001",
            "localhost:6002"
        ]

    def JoinGame(self, request, context):

        with self.lock:
            pid = str(uuid.uuid4())[:8]

            if not self.players:
                self.it_player = pid
                is_it = True
            else:
                is_it = False

            region = self.regions[len(self.players) % 2]

            self.players[pid] = region

            print(f"[MASTER] {request.name} joined as {pid}")

            return disttag_pb2.JoinResponse(
                player_id=pid,
                region_addr=region,
                is_it=is_it
            )

    def ReportTag(self, request, context):

        with self.lock:
            self.it_player = request.tagged

            print(f"[MASTER] {request.tagger} tagged {request.tagged}")

            return disttag_pb2.Ack(status="OK")

    def GetItPlayer(self, request, context):

        return disttag_pb2.ItInfo(player_id=self.it_player)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    disttag_pb2_grpc.add_GameMasterServicer_to_server(
        GameMaster(), server
    )

    server.add_insecure_port("[::]:5000")
    server.start()

    print("GameMaster running on :5000")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
