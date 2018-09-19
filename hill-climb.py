import chess

b = chess.Board(8)
b.random_fill(8)

score_old = -1
score = 0

while score > score_old:
    score_old = score
    for piece in b.pieces:
        max_piece = None
        max_x = None
        max_y = None
        try:
            piece.move(piece.x + 1, piece.y)
            ff, kill = b.count_total_targets()
            if kill - ff > score:
                score = kill - ff
                max_piece = piece
                max_x = piece.x
                max_y = piece.y
            piece.move(piece.x - 1, piece.y)            
        except:
            pass
        try:
            piece.move(piece.x - 1, piece.y)
            ff, kill = b.count_total_targets()
            if kill - ff > score:
                score = kill - ff
                max_piece = piece
                max_x = piece.x
                max_y = piece.y
            piece.move(piece.x + 1, piece.y)            
        except:
            pass
        try:
            piece.move(piece.x, piece.y + 1)
            ff, kill = b.count_total_targets()
            if kill - ff > score:
                score = kill - ff
                max_piece = piece
                max_x = piece.x
                max_y = piece.y
            piece.move(piece.x, piece.y - 1)            
        except:
            pass
        try:
            piece.move(piece.x, piece.y - 1)
            ff, kill = b.count_total_targets()
            if kill - ff > score:
                score = kill - ff
                max_piece = piece
                max_x = piece.x
                max_y = piece.y
            piece.move(piece.x, piece.y + 1)            
        except:
            pass
        if max_piece:
            max_piece.move(max_x, max_y)

print(b.count_total_targets())