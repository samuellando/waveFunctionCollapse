from EigenTile import EigenTile
from Board import Board
import os
import cProfile

def run():
    d = "pipes"
    images = os.listdir("tiles/"+d)
    subtiles = []
    for t in images:
        subtiles.append(EigenTile("tiles/" + d + "/" + t))

    tile = EigenTile.combine(subtiles)

    board = Board(tile, 100)
    for _ in board.getUpdates():
        pass


if __name__ == "__main__":
    cProfile.run('run()', "profile")