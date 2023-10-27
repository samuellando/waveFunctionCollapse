from EigenTile import EigenTile
from Board import Board
import time

import os
if __name__ == "__main__":
    d = "pipes"
    images = os.listdir("tiles/"+d)
    subtiles = []
    for t in images:
        subtiles.append(EigenTile("tiles/" + d + "/" + t))

    tile = EigenTile.combine(subtiles)

    with open("out.csv", "w") as f:
        for i in range(1, 101):
            board = Board(tile, i)
            start = time.time()
            for updates in board.getUpdates():
                pass
            print(i, time.time() - start, sep=", ")
            f.write(str(i) + ", " + str(time.time() - start) + "\n")

