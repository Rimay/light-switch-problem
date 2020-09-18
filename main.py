from IPython import  embed
import random, copy


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.n = len(board)
        self.m = len(board[0]) if self.n!=0 else 0

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row-1>=0:
            self.board[row-1][col] = not self.board[row-1][col]
        if col-1>=0:
            self.board[row][col-1] = not self.board[row][col-1]
        if row+1<self.n:
            self.board[row+1][col] = not self.board[row+1][col]
        if col+1<self.m:
            self.board[row][col+1] = not self.board[row][col+1]

    def scramble(self):
        for i in range(self.n):
            for j in range(self.m):
                if random.random()<0.5:
                    self.perform_move(i,j)

    def is_solved(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j]:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self.board)

    def successors(self):
        for i in range(self.n):
            for j in range(self.m):
                ret = copy.deepcopy(self)
                ret.perform_move(i,j)
                yield (i,j), ret

    def find_solution(self):
        press = [[0 for j in range(self.m+2)] for i in range(self.n+1)]
        def ok():
            for i in range(2, self.n+1):
                for j in range(1, self.m+1):
                    press[i][j] = (self.board[i-2][j-1]+press[i-1][j]+press[i-1][j-1]+press[i-1][j+1]) % 2
            for j in range(1, self.m+1):
                if self.board[self.n-1][j-1] != (press[self.n][j-1]+press[self.n][j]+\
                                        press[self.n][j+1]+press[self.n-1][j]) % 2:
                    return False
            return True
        while not ok():
            """
                enumerate from 0000...00 to 1111...11
            """
            press[1][1] += 1
            c=1
            while c<=self.m and press[1][c] > 1:
                press[1][c] = 0
                c += 1
                if c == self.m+1:
                    return None
                press[1][c] += 1

        ret = []
        for i in range(1, self.n+1):
            for j in range(1, self.m+1):
                if press[i][j]==1:
                    ret.append((i-1,j-1))
        return ret


def create_puzzle(rows, cols):
    board = [[False for j in range(cols)] for i in range(rows)]
    p = LightsOutPuzzle(board)
    return p


if __name__ == '__main__':
    p = create_puzzle(2,3)
    for i in range(2):
        for j in range(3):
            p.perform_move(i,j)  
    print(p.find_solution())
    solve_identical_disks(5,3)
    solve_distinct_disks(5,2)
    # embed()  
    
