import pygame
from EigenTile import EigenTile
from Board import Board

#pygame.init()

import os
import sys
if __name__ == "__main__":
    w = 10
    d = sys.argv[1]
    images = os.listdir("tiles/"+d)
    subtiles = []
    for t in images:
        subtiles.append(EigenTile("tiles/" + d + "/" + t))

    tile = EigenTile.combine(subtiles)
    board = Board(tile, w)

    display_width = w * 10
    display_height = w * 10
    #display = pygame.display.set_mode((display_width,display_height))
    #clock = pygame.time.Clock()

    black = (0,0,0)
    white = (255,255,255)
    #font = pygame.font.SysFont('freesans', 6)
        
    run = False
    #display.fill(black)
    for updates in board.getUpdates():
        for u in updates:
            print(u.tile.entropy(), end=" ")
        print()


        """
        for i, r in enumerate(m):
            for j, c in enumerate(r):
                if c is not None:
                    if len(c) == 1 and c[0]["collapsed"]:
                        display.blit(c[0]["image"], (j*10, i*10))
                    else:
                        # print the len of c
                        img = font.render(str(len(c)), True, white)
                        display.fill(black, (j*10, i*10, 10, 10))
                        display.blit(img, (j*10 + 2, i*10 + 2))

        pygame.display.update()
        """