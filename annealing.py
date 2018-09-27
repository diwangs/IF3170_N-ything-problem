import chess
import decimal
import math
import random

board = chess.Board(8)
board.random_fill(8)
print("Initial (ff, kill):", board.count_total_targets())
print(board)

temperature = 4000
ratio = 0.99

ff, kill = board.count_total_targets()
score_old = ff - kill - 1
score = kill - ff

while score > score_old: # While there exist an improvement that can be made...
    score_old = score
    max_piece, max_x, max_y = None, None, None
    for piece in board.pieces: # for every piece in the board
        for delta_x in range(-1, 2): # Check the adjacent place
            for delta_y in range(-1, 2):
                try: 
                    piece.move(piece.x + delta_x, piece.y + delta_y) # Move temporarily
                    ff, kill = board.count_total_targets() # Check if it's valid and whether it will give best result
                    dE = kill - ff - score
                    # probability = decimal.Decimal(decimal.Decimal(math.e) ** (decimal.Decimal(-dE) * decimal.Decimal(temperature)))
                    if dE > 0 or random.uniform(0, 10) < 0.1: # if yes, store the movement
                        score, max_piece, max_x, max_y = kill - ff, piece, piece.x, piece.y 
                    
                    piece.move(piece.x - delta_x, piece.y - delta_y) # Restore the previous placement
                except ValueError: pass # if movement not valid, pass
    if max_piece: max_piece.move(max_x, max_y) # Update the board to the best possible state, if a better state found

# print(b)
print("Simulated Annealing (ff, kill):", board.count_total_targets())
print(board)