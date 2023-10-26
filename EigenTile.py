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
        if self.collapsed:
            return self.states[0]
        else:
            self.collapse()
            return self.states[0]

    def entropy(self):
        return len(self.states)

    def __lt__(self, other):
        return self.entropy() < other.entropy()

    def __gt__(self, other):
        return self.entropy() > other.entropy()
    
    def __eq__(self, other):
        return self.entropy() == other.entropy()
    
    def __le__(self, other):
        return self.entropy() <= other.entropy()
    
    def __ge__(self, other):
        return self.entropy() >= other.entropy()
    
    def __ne__(self, other):
        return self.entropy() != other.entropy()

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
        def __init__(self, data):
            self.top = data[0, :]
            self.bottom = data[-1, :]
            self.left = data[:, 0]
            self.right = data[:, -1]
            self.image = pygame.image.frombytes(data.tobytes(), (len(data[0]), len(data)), "RGBA")

        def fits(self, tile, socket):
            match socket:
                case Sockets.TOP:
                    return np.array_equiv(self.top, tile.bottom)
                case Sockets.BOTTOM:
                    return np.array_equiv(self.bottom, tile.top)
                case Sockets.LEFT:
                    return np.array_equiv(self.left, tile.right)
                case Sockets.RIGHT:
                    return np.array_equiv(self.right, tile.left)