import grpc
from concurrent import futures
import threading
import math

import disttag_pb2
import disttag_pb2_grpc


WORLD_H = 50
WORLD_W = 100


class Region(disttag_pb2_grpc.RegionServerServicer):

    def __init__(self, name, x_min, x_max):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.players = {}
        self.lock = threading.Lock()

        self.master = grpc.insecure_channel("localhost:5000")
        self.master_stub = disttag_pb2_grpc.GameMasterStub(self.master)

    def AddPlayer(self, request, context):

        with self.lock:
            self.players[request.player_id] = [request.x, request.y]

            print(f"[{self.name}] Added {request.player_id}")

        return disttag_pb2.Ack(status="OK")

    def RemovePlayer(self, request, context):

        with self.lock:
            if request.player_id in self.players:
                del self.players[request.player_id]

        return disttag_pb2.Ack(status="OK")

    def Move(self, request, context):

        with self.lock:

            if request.player_id not in self.players:
                return disttag_pb2.MoveResponse()

            pos = self.players[request.player_id]

            pos[0] += request.dx
            pos[1] += request.dy

            pos[0] = max(self.x_min, min(self.x_max, pos[0]))
            pos[1] = max(0, min(WORLD_H, pos[1]))

            self.players[request.player_id] = pos

            tagged = self.check_tag(request.player_id)

            return disttag_pb2.MoveResponse(
                x=pos[0],
                y=pos[1],
                tagged=tagged
            )

    def check_tag(self, pid):

        it = self.master_stub.GetItPlayer(
            disttag_pb2.Empty()
        ).player_id

        if it != pid:
            return False

        x1, y1 = self.players[pid]

        for other, pos in self.players.items():

            if other == pid:
                continue

            x2, y2 = pos

            d = math.dist((x1, y1), (x2, y2))

            if d <= 1:

                self.master_stub.ReportTag(
                    disttag_pb2.TagEvent(
                        tagger=pid,
                        tagged=other
                    )
                )

                return True

        return False


def serve(name, port, x_min, x_max):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    disttag_pb2_grpc.add_RegionServerServicer_to_server(
        Region(name, x_min, x_max), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"{name} running on :{port}")

    server.wait_for_termination()


if __name__ == "__main__":

    import sys

    name = sys.argv[1]
    port = int(sys.argv[2])
    x_min = int(sys.argv[3])
    x_max = int(sys.argv[4])

    serve(name, port, x_min, x_max)
