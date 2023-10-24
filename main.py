import random
import imageio.v3 as iio
import pygame

pygame.init()

def collapse(options, w, h):
    outcomes = [[options.copy() for _ in range(w)] for _ in range(h)]
    mask = outcomes

    s = []
    while True:
        if len(s) == 0:
            for i, r in enumerate(outcomes):
                for j, l in enumerate(r):
                    s.append([l, i, j])
            s = list(filter(lambda x: len(x[0]) >= 1 and not x[0][0]["collapsed"], s))
            if len(s) == 0:
                break
        m = min(s, key=lambda x: len(x[0]))
        options = list(filter(lambda x: len(x[0]) == len(m[0]), s))
        p = random.choice(options)
        # Randomly choose from the possible outcomes
        y = random.choice(p[0]).copy()
        # Update the pixel
        y["collapsed"] = True
        p[0] = [y]
        outcomes[p[1]][p[2]] = [y]
        mask[p[1]][p[2]] = [y]
        # Update the surrounding pixels
        s = []
        if p[1] > 0 and len(outcomes[p[1]-1][p[2]]) > 1:
            l = len(outcomes[p[1]-1][p[2]])
            outcomes[p[1]-1][p[2]] = list(filter(lambda x: x["adj"][2] == y["adj"][0], outcomes[p[1]-1][p[2]]))
            mask[p[1]-1][p[2]] = outcomes[p[1]-1][p[2]]
            if l != len(outcomes[p[1]-1][p[2]]) and len(outcomes[p[1]-1][p[2]]) >= 1:
                s.append([outcomes[p[1]-1][p[2]], p[1]-1, p[2]])
        if p[1] < h-1 and len(outcomes[p[1]+1][p[2]]) > 1:
            l = len(outcomes[p[1]+1][p[2]])
            outcomes[p[1]+1][p[2]] = list(filter(lambda x: x["adj"][0] == y["adj"][2], outcomes[p[1]+1][p[2]]))
            mask[p[1]+1][p[2]] = outcomes[p[1]+1][p[2]]
            if l != len(outcomes[p[1]+1][p[2]]) and len(outcomes[p[1]+1][p[2]]) >= 1:
                s.append([outcomes[p[1]+1][p[2]], p[1]+1, p[2]])
        if p[2] > 0 and len(outcomes[p[1]][p[2]-1]) > 1:
            l = len(outcomes[p[1]][p[2]-1])
            outcomes[p[1]][p[2]-1] = list(filter(lambda x: x["adj"][1] == y["adj"][3], outcomes[p[1]][p[2]-1]))
            mask[p[1]][p[2]-1] = outcomes[p[1]][p[2]-1]
            if l != len(outcomes[p[1]][p[2]-1]) and len(outcomes[p[1]][p[2]-1]) >= 1:
                s.append([outcomes[p[1]][p[2]-1], p[1], p[2]-1])
        if p[2] < w-1 and len(outcomes[p[1]][p[2]+1]) > 1:
            l = len(outcomes[p[1]][p[2]+1])
            outcomes[p[1]][p[2]+1] = list(filter(lambda x: x["adj"][3] == y["adj"][1], outcomes[p[1]][p[2]+1]))
            mask[p[1]][p[2]+1] = outcomes[p[1]][p[2]+1]
            if l != len(outcomes[p[1]][p[2]+1]) and len(outcomes[p[1]][p[2]+1]) >= 1:
                s.append([outcomes[p[1]][p[2]+1], p[1], p[2]+1])
        yield mask
        mask = [[None] * w for _ in range(h)]

    return outcomes

def toHex(a):
    s = ""
    for rgba in a:
        for v in rgba[:3]:
            s += hex(v).replace("0x", "").zfill(2)
    return s

import re
def allRoations(a):
    for tile in a:
        adj = tile["adj"]
        for i in range(4):
            yield {
                "collapsed": tile["collapsed"],
                "title": tile["title"],
                "image": pygame.transform.rotate(tile["image"], i * 90),
                "adj": adj
            }
            adj = adj[1:] + adj[:1]
            adj[1] = "".join(re.findall("......", adj[1])[::-1])
            adj[3] = "".join(re.findall("......", adj[3])[::-1])

def allFlips(a):
    for tile in a:
        adj = tile["adj"]
        yield tile
        adj[0] = "".join(re.findall("......", adj[0])[::-1])
        adj[2] = "".join(re.findall("......", adj[2])[::-1])
        yield {
            "collapsed": tile["collapsed"],
            "title": tile["title"],
            "image": pygame.transform.flip(tile["image"], True, False),
            "adj": [adj[0], adj[3], adj[2], adj[1]]
        }

import os
import sys
if __name__ == "__main__":
    w = 100
    d = sys.argv[1]
    tiles = os.listdir("tiles/"+d)
    options = []
    for t in tiles:
        im = iio.imread("tiles/" + d + "/" + t)
        top = toHex(im[0, :])
        bottom = toHex(im[-1, :])
        left = toHex(im[:, 0])
        right = toHex(im[:, -1])
        options.append({
            "collapsed": False,
            "title": t,
            "image": pygame.image.load("tiles/" + d + "/" + t),
            "adj": [top, right, bottom, left]
        })


    display_width = w * 10
    display_height = w * 10
    display = pygame.display.set_mode((display_width,display_height))
    clock = pygame.time.Clock()

    black = (0,0,0)
    white = (255,255,255)
    font = pygame.font.SysFont('freesans', 6)
    options = list(allRoations(options))
    options = list(allFlips(options))
        
    run = False
    display.fill(black)
    for m in collapse(options, w, w):
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

    while True:
        pass

