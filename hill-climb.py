import chess

b = chess.Board(8)
b.random_fill(8)
print("Initial (ff, kill):", b.count_total_targets())

score_old = -1
score = 0

while score > score_old:
    score_old = score
    max_piece, max_x, max_y = None, None, None
    for piece in b.pieces: # for every piece in the board
        for delta_x in range(-1, 2): # Check the adjacent place
            for delta_y in range(-1, 2):
                try: 
                    piece.move(piece.x + delta_x, piece.y + delta_y) # Move temporarily
                    ff, kill = b.count_total_targets() # Check if it's valid and whether it will give best result
                    if kill - ff > score: # if yes, store the movement
                        score, max_piece, max_x, max_y = kill - ff, piece, piece.x, piece.y 
                    piece.move(piece.x - delta_x, piece.y - delta_y) # Restore the previous placement
                except ValueError: pass # If movement not valid, pass
    if max_piece: max_piece.move(max_x, max_y) # Update the board to the best possible state, if a better state found

# print(b)
print("Hill-climbed (ff, kill):", b.count_total_targets())