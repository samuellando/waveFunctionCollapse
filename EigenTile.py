import imageio.v3 as iio
import pygame
import enum
import numpy as np
import random

class Sockets(enum.Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

class EigenTile:
    def __init__(self, file, states = None):
        if states is not None:
            self.states = states
        else:
            self.states = list(EigenTile.generateAllStates(file))
        self.collapsed = False

    def isCollapsed(self):
        return self.collapsed or len(self.states) == 0

    def collapse(self, tile=None, socket=None):
        if self.isCollapsed():
            return
        if tile is not None and socket is not None:
            self.states = list(filter(lambda x: x.fits(tile.observe(), socket), self.states))
        else:
            self.states = [random.choice(self.states)]
            self.collapsed = True

    def observe(self):
        if len(self.states) == 0:
            return None
        if self.collapsed:
            return self.states[0]
        else:
            self.collapse()
            return self.states[0]

    def entropy(self):
        return len(self.states)

    def clone(self):
        return EigenTile(None, self.states.copy())

    @classmethod
    def generateAllStates(cls, file):
        im = iio.imread(file)
        for i in range(4):
            rim = np.rot90(im, i)
            yield EigenTile.Tile(rim)
            fim = np.flipud(rim)
            yield EigenTile.Tile(fim)

    @classmethod
    def combine(cls, it):
        et = EigenTile(None, [])
        for tile in it:
            et.states.extend(tile.states)

        return et

    class Tile:
        sockets = {}

        def __init__(self, data):
            top = data[0, :].tobytes()
            if top in EigenTile.Tile.sockets:
                self.top = EigenTile.Tile.sockets[top]
            else:
                self.top = len(EigenTile.Tile.sockets)
                EigenTile.Tile.sockets[top] = len(EigenTile.Tile.sockets)
            bottom = data[-1, :].tobytes()
            if bottom in EigenTile.Tile.sockets:
                self.bottom = EigenTile.Tile.sockets[bottom]
            else:
                self.bottom = len(EigenTile.Tile.sockets)
                EigenTile.Tile.sockets[bottom] = len(EigenTile.Tile.sockets)
            left = data[:, 0].tobytes()
            if left in EigenTile.Tile.sockets:
                self.left = EigenTile.Tile.sockets[left]
            else:
                self.left = len(EigenTile.Tile.sockets)
                EigenTile.Tile.sockets[left] = len(EigenTile.Tile.sockets)
            right = data[:, -1].tobytes()
            if right in EigenTile.Tile.sockets:
                self.right = EigenTile.Tile.sockets[right]
            else:
                self.right = len(EigenTile.Tile.sockets)
                EigenTile.Tile.sockets[right] = len(EigenTile.Tile.sockets)

            self.image = pygame.image.frombytes(data.tobytes(), (len(data[0]), len(data)), "RGBA")

        def fits(self, tile, socket):
            match socket:
                case Sockets.TOP:
                    return self.top == tile.bottom
                case Sockets.BOTTOM:
                    return self.bottom == tile.top
                case Sockets.LEFT:
                    return self.left == tile.right
                case Sockets.RIGHT:
                    return self.right == tile.left
