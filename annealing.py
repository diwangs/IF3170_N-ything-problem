import chess
import decimal
import math
import random

board = chess.Board(8)
# board.random_fill(20)
board.fill_piece_from_file("input")
print("Initial (ff, kill):", board.count_total_targets())
print(board)

temperature = 4000
ratio = 0.99

ff, kill = board.count_total_targets()
score_old = ff - kill - 1
score = kill - ff

for i in range(1, 100):  # While there exist an improvement that can be made...
    score_old = score
    max_piece, max_x, max_y = None, None, None
    for piece in board.pieces:  # for every piece in the board
        for delta_x in range(-1, 2):  # Check the adjacent place
            for delta_y in range(-1, 2):
                try:
                    piece.move(piece.x + delta_x, piece.y +
                               delta_y)  # Move temporarily
                    # Check if it's valid and whether it will give best result
                    ff, kill = board.count_total_targets()
                    delta_e = kill - ff - score
                    # probability = decimal.Decimal(decimal.Decimal(math.e) ** (decimal.Decimal(-delta_e) * decimal.Decimal(temperature)))

                    # if yes, store the movement
                    if delta_e > 0 or random.uniform(0, 10) < 0.1:
                        score, max_piece, max_x, max_y = kill - ff, piece, piece.x, piece.y

                    # Restore the previous placement
                    piece.move(piece.x - delta_x, piece.y - delta_y)
                except ValueError:
                    pass  # if movement not valid, pass
    if max_piece:
        # Update the board to the best possible state, if a better state found
        max_piece.move(max_x, max_y)

# print(b)
print("Simulated Annealing (ff, kill):", board.count_total_targets())
print(board)
