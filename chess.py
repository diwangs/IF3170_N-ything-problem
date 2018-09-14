'''
Notes:
* There is no explicit getter and setter function, you define the getter by the '@property' wrapper and the
    setter by the '@<your-attribute>.setter' wrapper
* Private attributes are conventioned with the __ prefix
* Protected attributes are conventioned with the _ prefix
* ff = friendly fire, amount of the pieces with the same color that are in the killing zone of a given piece 
* kill = amount of the pieces, with an opposite color, that can be eliminated from that position
'''

from random import randint, getrandbits

class Board:
    def __init__(self, size):
        self.__size = size
        self.__pieces = []
    
    @property
    def size(self):
        return self.__size

    @property
    def pieces(self):
        return self.__pieces

    def add_piece(self, piece):
        if piece.x < 0 or piece.x >= self.size or piece.y < 0 or piece.y >= self.size: 
            raise ValueError("Piece position is out of bound")
        for placed_piece in self.pieces:
            if placed_piece.x == piece.x and placed_piece.y == piece.y:
                raise ValueError("Position already filled")
        self.pieces.append(piece) 

    def random_fill(self, count):
        while len(self.pieces) < count:
            try:
                choice = randint(0, 3)
                if choice == 0:
                    self.add_piece(Queen(bool(getrandbits(1)), randint(0, self.size - 1), randint(0, self.size - 1)))
                elif choice == 1:
                    self.add_piece(Bishop(bool(getrandbits(1)), randint(0, self.size - 1), randint(0, self.size - 1)))
                elif choice == 2:
                    self.add_piece(Rook(bool(getrandbits(1)), randint(0, self.size - 1), randint(0, self.size - 1)))
                else:
                    self.add_piece(Knight(bool(getrandbits(1)), randint(0, self.size - 1), randint(0, self.size - 1)))
            except:
                pass

    def count_total_targets(self):
        ff_tot = 0 # ff = friendly fire
        kill_tot = 0
        for piece in self.pieces:
            ff, kill = piece.count_targets(self)
            ff_tot += ff
            kill_tot += kill
        return ff_tot, kill_tot
    
    def __str__(self):
        # To be implemented
        pass


class Piece:
    def __init__(self, color, x, y):
        self._color = color # True = white
        self._x = x
        self._y = y
        # Using a chessboard convention, (0, 0) is the bottom-left corner
    
    @property
    def color(self):
        return self._color
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def move(self, x, y):
        self.x = x
        self.y = y


def count_hv_targets(piece, board):
    # Count horizontal and vertical targets
    ff = 0 
    kill = 0 
    s_check = True # Whether we should continue checking south
    n_check = True
    w_check = True
    e_check = True
    for target in board.pieces:
        for i in range(1, board.size):
            if piece.x - i >= 0 and s_check:
                if target.x == piece.x - i and target.y == piece.y:
                    if target.color == piece.color: ff += 1 
                    else: kill += 1
                    s_check = False
                    continue
            if piece.x + i < board.size and n_check:
                if target.x == piece.x + i and target.y == piece.y:
                    if target.color == piece.color: ff += 1 
                    else: kill += 1
                    n_check = False
                    continue
            if piece.y - i >= 0 and w_check:
                if target.x == piece.x and target.y == piece.y - i:
                    if target.color == piece.color: ff += 1 
                    else: kill += 1
                    w_check = False
                    continue
            if piece.y + i < board.size and e_check:
                if target.x == piece.x and target.y == piece.y + i:
                    if target.color == piece.color: ff += 1 
                    else: kill += 1
                    e_check = False
    return ff, kill


def count_diag_targets(piece, board):
    # Count diagonal targets
    ff = 0
    kill = 0
    sw_check = True # Whether we should continue checking southwest
    nw_check = True
    se_check = True
    ne_check = True
    for target in board.pieces:
        for i in range(1, board.size):
            if piece.x - i >= 0:
                if piece.y - i >= 0 and sw_check:
                    if target.x == piece.x - i and target.y == piece.y - i: 
                        if target.color == piece.color: ff += 1
                        else: kill += 1
                        sw_check = False
                        continue
                if piece.y + i < board.size and nw_check:
                    if target.x == piece.x - i and target.y == piece.y + i:
                        if target.color == piece.color: ff += 1
                        else: kill += 1
                        nw_check = False
                        continue
            if piece.x + i < board.size:
                if piece.y - i >= 0 and se_check:
                    if target.x == piece.x + i and target.y == piece.y - i: 
                        if target.color == piece.color: ff += 1
                        else: kill += 1
                        se_check = False
                        continue
                if piece.y + i < board.size and ne_check:
                    if target.x == piece.x + i and target.y == piece.y + i: 
                        if target.color == piece.color: ff += 1
                        else: kill += 1
                        ne_check = False
    return ff, kill
        

class Queen(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
    
    def count_targets(self, board): 
        ff_hv, kill_hv = count_hv_targets(self, board)
        ff_diag, kill_diag = count_diag_targets(self, board)
        return ff_hv + ff_diag, kill_hv + kill_diag


class Rook(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
    
    def count_targets(self, board): 
        return count_hv_targets(self, board)


class Bishop(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
    
    def count_targets(self, board): 
        return count_diag_targets(self, board)


class Knight(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def count_targets(self, board): 
        ff = 0
        kill = 0
        for target in board.pieces:
            if target == self: continue
            if self.x - 2 >= 0:
                if self.y - 1 >= 0:
                    if target.x == self.x - 2 and target.y == self.y - 1:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
                if self.y + 1 < board.size:
                    if target.x == self.x - 2 and target.y == self.y + 1:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
            if self.x - 1 >= 0:
                if self.y - 2 >= 0:
                    if target.x == self.x - 1 and target.y == self.y - 2:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
                if self.y + 2 < board.size:
                    if target.x == self.x - 1 and target.y == self.y + 2:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
            if self.x + 1 < board.size:
                if self.y - 2 >= 0:
                    if target.x == self.x + 1 and target.y == self.y - 2:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
                if self.y + 2 < board.size:
                    if target.x == self.x + 1 and target.y == self.y + 2:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
            if self.x + 2 < board.size:
                if self.y - 1 >= 0:
                    if target.x == self.x + 2 and target.y == self.y - 1:
                        if target.color == self.color: ff += 1
                        else: kill += 1
                        continue
                if self.y + 1 < board.size:
                    if target.x == self.x + 2 and target.y == self.y + 1:
                        if target.color == self.color: ff += 1
                        else: kill += 1
        return ff, kill


# Quick testing, supposed to be (1, 0)      
b = Board(8)
b.random_fill(8)
print(b.count_total_targets())