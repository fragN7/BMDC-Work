import grpc
import random
import sys

import disttag_pb2
import disttag_pb2_grpc


def main():

    name = input("Name: ")

    master = grpc.insecure_channel("localhost:5000")
    master_stub = disttag_pb2_grpc.GameMasterStub(master)

    join = master_stub.JoinGame(
        disttag_pb2.PlayerInfo(name=name)
    )

    pid = join.player_id
    region_addr = join.region_addr
    is_it = join.is_it

    print(f"ID: {pid}")
    print(f"Region: {region_addr}")
    print(f"IT: {is_it}")

    region = grpc.insecure_channel(region_addr)
    region_stub = disttag_pb2_grpc.RegionServerStub(region)

    x = random.randint(0, 99)
    y = random.randint(0, 49)

    region_stub.AddPlayer(
        disttag_pb2.PlayerState(
            player_id=pid,
            x=x,
            y=y
        )
    )

    print("Controls: W A S D | Q to quit")

    while True:

        key = input("> ").lower()

        if key == "q":
            break

        dx = dy = 0

        if key == "w": dy = -1
        if key == "s": dy = 1
        if key == "a": dx = -1
        if key == "d": dx = 1

        res = region_stub.Move(
            disttag_pb2.MoveRequest(
                player_id=pid,
                dx=dx,
                dy=dy
            )
        )

        print(f"Pos: ({res.x}, {res.y})")

        if res.tagged:
            print("🎯 You tagged someone!")

    region_stub.RemovePlayer(
        disttag_pb2.PlayerId(player_id=pid)
    )


if __name__ == "__main__":
    main()
