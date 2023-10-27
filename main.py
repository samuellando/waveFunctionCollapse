import pygame
from EigenTile import EigenTile
from Board import Board

pygame.init()

import os
import sys
if __name__ == "__main__":
    w = 100
    d = sys.argv[1]
    images = os.listdir("tiles/"+d)
    subtiles = []
    for t in images:
        subtiles.append(EigenTile("tiles/" + d + "/" + t))

    tile = EigenTile.combine(subtiles)
    board = Board(tile, w)

    display_width = w * 10
    display_height = w * 10
    display = pygame.display.set_mode((display_width,display_height))
    clock = pygame.time.Clock()

    black = (0,0,0)
    white = (255,255,255)
    font = pygame.font.SysFont('freesans', 6)
        
    run = False
    display.fill(black)
    for updates in board.getUpdates():
        for u in updates:
            if u.tile.isCollapsed() and u.tile.observe() is not None:
                display.blit(u.tile.observe().image, (u.x * 10, u.y * 10))
            else:
                # print the len of c
                img = font.render(str(u.tile.entropy()), True, white)
                display.fill(black, (u.x*10, u.y*10, 10, 10))
                display.blit(img, (u.x*10 + 2, u.y*10 + 2))

        pygame.display.update()

    input()
