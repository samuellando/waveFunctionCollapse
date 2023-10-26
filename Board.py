from EigenTile import EigenTile, Sockets
import heapq

class Board:
    class Update:
        def __init__(self, tile, x, y):
            self.tile = tile
            self.x = x
            self.y = y

    def __init__(self, tile: EigenTile, w, h=None):
        self.w = w
        self.h = h if h is not None else w
        self.board = [[tile.clone() for _ in range(self.w)] for _ in range(self.h)]

    def __getitem__(self, item):
        return self.board[item]

    def getUpdates(self):
        updates = []
        s = []
        for y in range(self.h):
            for x in range(self.w):
                updates.append(Board.Update(self.board[y][x], x, y))
                s.append((self.board[y][x], (x, y)))

        yield updates

        heapq.heapify(s)
        while len(s) > 0:
            updates = []

            p = heapq.heappop(s)[1]
            x = p[0]
            y = p[1]
            selection = self.board[y][x]
            selection.collapse()
            updates.append(Board.Update(selection, x, y))

            if x > 0 and not self.board[y][x-1].isCollapsed():
                self.board[y][x-1].collapse(selection, Sockets.RIGHT)
                updates.append(Board.Update(self.board[y][x-1], x-1, y))
            if x < len(self.board[0]) - 1 and not self.board[y][x+1].isCollapsed():
                self.board[y][x+1].collapse(selection, Sockets.LEFT)
                updates.append(Board.Update(self.board[y][x+1], x+1, y))
            if y > 0 and not self.board[y-1][x].isCollapsed():
                self.board[y-1][x].collapse(selection, Sockets.BOTTOM)
                updates.append(Board.Update(self.board[y-1][x], x, y-1))
            if y < len(self.board) - 1 and not self.board[y+1][x].isCollapsed():
                self.board[y+1][x].collapse(selection, Sockets.TOP)
                updates.append(Board.Update(self.board[y+1][x], x, y+1))

            yield updates

            heapq.heapify(s)