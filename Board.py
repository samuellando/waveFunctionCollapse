from EigenTile import EigenTile, Sockets
import heapdict

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
        h = heapdict.heapdict()
        for y in range(self.h):
            for x in range(self.w):
                updates.append(Board.Update(self.board[y][x], x, y))
                h[(x, y)] = self.board[y][x].entropy()

        yield updates

        for _ in range(self.w * self.h):
            updates = []

            p, _ = h.popitem()
            x = p[0]
            y = p[1]
            selection = self.board[y][x]
            selection.collapse()
            updates.append(Board.Update(selection, x, y))

            if selection.observe() is not None:
                if x > 0 and not self.board[y][x-1].isCollapsed():
                    self.board[y][x-1].collapse(selection, Sockets.RIGHT)
                    updates.append(Board.Update(self.board[y][x-1], x-1, y))
                    h[(x-1, y)] = self.board[y][x-1].entropy()
                if x < len(self.board[0]) - 1 and not self.board[y][x+1].isCollapsed():
                    self.board[y][x+1].collapse(selection, Sockets.LEFT)
                    updates.append(Board.Update(self.board[y][x+1], x+1, y))
                    h[(x+1, y)] = self.board[y][x+1].entropy()
                if y > 0 and not self.board[y-1][x].isCollapsed():
                    self.board[y-1][x].collapse(selection, Sockets.BOTTOM)
                    updates.append(Board.Update(self.board[y-1][x], x, y-1))
                    h[(x, y-1)] = self.board[y-1][x].entropy()
                if y < len(self.board) - 1 and not self.board[y+1][x].isCollapsed():
                    self.board[y+1][x].collapse(selection, Sockets.TOP)
                    updates.append(Board.Update(self.board[y+1][x], x, y+1))
                    h[(x,y+1)] = self.board[y+1][x].entropy()

            yield updates