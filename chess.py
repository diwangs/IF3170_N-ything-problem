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
import pickle


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

    def fill_piece_from_file(self, filename):
        with open(filename, "r") as f:
            s = f.read()
            print("Input file:\n{}".format(s))
            s = [l.strip().split()
                 for l in s.upper().strip().split('\n')]
            for l in s:
                color, piece, count = l[0], l[1], int(l[2])
                is_white = (color == "WHITE")
                if piece == "KNIGHT":
                    piece_class = Knight
                elif piece == "BISHOP":
                    piece_class = Bishop
                elif piece == "ROOK":
                    piece_class = Rook
                elif piece == "QUEEN":
                    piece_class = Queen
                else:
                    raise Exception("Invalid input file")
                for _ in range(count):
                    self.add_piece(piece_class(self, is_white, 0, 0))
            self.conflict_resolve()

    def is_placement_valid(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        for placed_piece in self.pieces:
            if placed_piece.x == x and placed_piece.y == y:
                return False
        return True

    # doesn't need check position is occupied
    # use conflict_resolve
    def add_piece(self, piece):
        # if self.is_placement_valid(piece.x, piece.y):
        self.pieces.append(piece)
        # else:
        #     raise ValueError("Piece's position isn't valid")

    def random_fill(self, count):
        while len(self.pieces) < count:
            try:
                choice = randint(0, 3)
                if choice == 0:
                    self.add_piece(Queen(self, bool(getrandbits(1)), randint(
                        0, self.size - 1), randint(0, self.size - 1)))
                elif choice == 1:
                    self.add_piece(Bishop(self, bool(getrandbits(1)), randint(
                        0, self.size - 1), randint(0, self.size - 1)))
                elif choice == 2:
                    self.add_piece(Rook(self, bool(getrandbits(1)), randint(
                        0, self.size - 1), randint(0, self.size - 1)))
                else:
                    self.add_piece(Knight(self, bool(getrandbits(1)), randint(
                        0, self.size - 1), randint(0, self.size - 1)))
            except Exception as e:
                pass
        self.conflict_resolve()
        # for i in range(count):
        #     self.add_piece(Queen(self, 0, randint(0, self.size - 1),randint(0, self.size - 1)))

    def count_total_targets(self):
        ff_tot = 0  # ff = friendly fire
        kill_tot = 0
        for piece in self.pieces:
            ff, kill = piece.count_targets()
            ff_tot += ff
            kill_tot += kill
        return ff_tot, kill_tot

    def new_random_state(self):
        temp = pickle.loads(pickle.dumps(self))
        for piece in temp.pieces:
            piece.random_move()
        return temp

    def conflict_resolve(self):
        for i in range(len(self.pieces)):
            for j in range(i + 1, len(self.pieces)):
                while (self.pieces[i].x == self.pieces[j].x and self.pieces[i].y == self.pieces[j].y):
                    self.pieces[i].random_move()

    def __str__(self):
        board = []
        for i in range(0, 8):
            board.append([])
            for j in range(0, 8):
                board[i].append('.')

        for piece in self.pieces:
            board[piece.x][piece.y] = piece.toStr()

        ret = ""
        for i in range(0, 8):
            for j in range(0, 8):
                ret = ret + board[i][j]
            ret = ret + "\n"

        return ret


class Piece:
    def __init__(self, board, color, x, y):
        self._board = board
        self._color = color  # True = white
        self._x = x
        self._y = y
        # Using a chessboard convention, (0, 0) is the bottom-left corner

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board):
        self._board = new_board

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
        if self.board.is_placement_valid(x, y):
            self.x = x
            self.y = y
        else:
            raise ValueError("Piece's position isn't valid")

    def random_move(self):
        while (True):
            try:
                self.move(randint(0, self.board.size - 1),
                          randint(0, self.board.size - 1))
                break
            except:
                pass


def count_hv_targets(board, piece):
    # Count horizontal and vertical targets
    ff = 0
    kill = 0
    s_check = True  # Whether we should continue checking south
    n_check = True
    w_check = True
    e_check = True
    for target in board.pieces:
        for i in range(1, board.size):
            if piece.x - i >= 0 and s_check:
                if target.x == piece.x - i and target.y == piece.y:
                    if target.color == piece.color:
                        ff += 1
                    else:
                        kill += 1
                    s_check = False
                    continue
            if piece.x + i < board.size and n_check:
                if target.x == piece.x + i and target.y == piece.y:
                    if target.color == piece.color:
                        ff += 1
                    else:
                        kill += 1
                    n_check = False
                    continue
            if piece.y - i >= 0 and w_check:
                if target.x == piece.x and target.y == piece.y - i:
                    if target.color == piece.color:
                        ff += 1
                    else:
                        kill += 1
                    w_check = False
                    continue
            if piece.y + i < board.size and e_check:
                if target.x == piece.x and target.y == piece.y + i:
                    if target.color == piece.color:
                        ff += 1
                    else:
                        kill += 1
                    e_check = False
    return ff, kill


def count_diag_targets(board, piece):
    # Count diagonal targets
    ff = 0
    kill = 0
    sw_check = True  # Whether we should continue checking southwest
    nw_check = True
    se_check = True
    ne_check = True
    for target in board.pieces:
        for i in range(1, board.size):
            if piece.x - i >= 0:
                if piece.y - i >= 0 and sw_check:
                    if target.x == piece.x - i and target.y == piece.y - i:
                        if target.color == piece.color:
                            ff += 1
                        else:
                            kill += 1
                        sw_check = False
                        continue
                if piece.y + i < board.size and nw_check:
                    if target.x == piece.x - i and target.y == piece.y + i:
                        if target.color == piece.color:
                            ff += 1
                        else:
                            kill += 1
                        nw_check = False
                        continue
            if piece.x + i < board.size:
                if piece.y - i >= 0 and se_check:
                    if target.x == piece.x + i and target.y == piece.y - i:
                        if target.color == piece.color:
                            ff += 1
                        else:
                            kill += 1
                        se_check = False
                        continue
                if piece.y + i < board.size and ne_check:
                    if target.x == piece.x + i and target.y == piece.y + i:
                        if target.color == piece.color:
                            ff += 1
                        else:
                            kill += 1
                        ne_check = False
    return ff, kill


class Queen(Piece):
    def __init__(self, board, color, x, y):
        Piece.__init__(self, board, color, x, y)

    def count_targets(self):
        ff_hv, kill_hv = count_hv_targets(self.board, self)
        ff_diag, kill_diag = count_diag_targets(self.board, self)
        return ff_hv + ff_diag, kill_hv + kill_diag

    def toStr(self):
        return "Q" if self.color else "q"


class Rook(Piece):
    def __init__(self, board, color, x, y):
        Piece.__init__(self, board, color, x, y)

    def count_targets(self):
        return count_hv_targets(self.board, self)

    def toStr(self):
        return "R" if self.color else "r"


class Bishop(Piece):
    def __init__(self, board, color, x, y):
        Piece.__init__(self, board, color, x, y)

    def count_targets(self):
        return count_diag_targets(self.board, self)

    def toStr(self):
        return "B" if self.color else "b"


class Knight(Piece):
    def __init__(self, board, color, x, y):
        Piece.__init__(self, board, color, x, y)

    def count_targets(self):
        ff = 0
        kill = 0
        for target in self.board.pieces:
            if target == self:
                continue
            if self.x - 2 >= 0:
                if self.y - 1 >= 0:
                    if target.x == self.x - 2 and target.y == self.y - 1:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
                if self.y + 1 < self.board.size:
                    if target.x == self.x - 2 and target.y == self.y + 1:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
            if self.x - 1 >= 0:
                if self.y - 2 >= 0:
                    if target.x == self.x - 1 and target.y == self.y - 2:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
                if self.y + 2 < self.board.size:
                    if target.x == self.x - 1 and target.y == self.y + 2:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
            if self.x + 1 < self.board.size:
                if self.y - 2 >= 0:
                    if target.x == self.x + 1 and target.y == self.y - 2:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
                if self.y + 2 < self.board.size:
                    if target.x == self.x + 1 and target.y == self.y + 2:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
            if self.x + 2 < self.board.size:
                if self.y - 1 >= 0:
                    if target.x == self.x + 2 and target.y == self.y - 1:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
                        continue
                if self.y + 1 < self.board.size:
                    if target.x == self.x + 2 and target.y == self.y + 1:
                        if target.color == self.color:
                            ff += 1
                        else:
                            kill += 1
        return ff, kill

    def toStr(self):
        return "K" if self.color else "k"
