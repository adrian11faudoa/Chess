import os
import sys

# Unicode chess pieces
PIECES = {
    'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
    'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟',
    '.':  '·'
}

def initial_board():
    board = [['.' for _ in range(8)] for _ in range(8)]
    order = ['R','N','B','Q','K','B','N','R']
    for i, p in enumerate(order):
        board[0][i] = 'b' + p
        board[7][i] = 'w' + p
    for i in range(8):
        board[1][i] = 'bP'
        board[6][i] = 'wP'
    return board

def print_board(board, selected=None, valid_moves=None):
    if valid_moves is None:
        valid_moves = []
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  ╔════════════════════════╗")
    print("  ║     PYTHON  CHESS      ║")
    print("  ╚════════════════════════╝\n")
    print("    a  b  c  d  e  f  g  h")
    print("  ┌──┬──┬──┬──┬──┬──┬──┬──┐")
    for r in range(8):
        row_label = 8 - r
        row_str = f"{row_label} │"
        for c in range(8):
            piece = board[r][c]
            symbol = PIECES.get(piece, piece)
            bg = ''
            if selected == (r, c):
                bg = '\033[43m'  # yellow bg for selected
            elif (r, c) in valid_moves:
                bg = '\033[42m'  # green bg for valid moves
            elif (r + c) % 2 == 0:
                bg = '\033[47m'  # light square
            else:
                bg = '\033[100m' # dark square
            reset = '\033[0m'
            row_str += f"{bg}{symbol} {reset}│"
        row_str += f" {row_label}"
        print(row_str)
        if r < 7:
            print("  ├──┼──┼──┼──┼──┼──┼──┼──┤")
    print("  └──┴──┴──┴──┴──┴──┴──┴──┘")
    print("    a  b  c  d  e  f  g  h\n")

def parse_pos(s):
    s = s.strip().lower()
    if len(s) != 2:
        return None
    col = ord(s[0]) - ord('a')
    row = 8 - int(s[1])
    if 0 <= row <= 7 and 0 <= col <= 7:
        return (row, col)
    return None

def pos_to_str(r, c):
    return chr(ord('a') + c) + str(8 - r)

def piece_color(piece):
    if piece == '.':
        return None
    return piece[0]

def get_valid_moves(board, r, c, en_passant_target=None, castling_rights=None):
    piece = board[r][c]
    if piece == '.':
        return []
    color = piece[0]
    ptype = piece[1]
    moves = []

    def in_bounds(x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def add_if_valid(x, y):
        if in_bounds(x, y):
            target = board[x][y]
            if target == '.' or piece_color(target) != color:
                moves.append((x, y))
                return target == '.'
        return False

    if ptype == 'P':
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        # Forward
        if in_bounds(r + direction, c) and board[r + direction][c] == '.':
            moves.append((r + direction, c))
            # Double push
            if r == start_row and board[r + 2*direction][c] == '.':
                moves.append((r + 2*direction, c))
        # Captures
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if in_bounds(nr, nc):
                if board[nr][nc] != '.' and piece_color(board[nr][nc]) != color:
                    moves.append((nr, nc))
                elif en_passant_target == (nr, nc):
                    moves.append((nr, nc))

    elif ptype == 'N':
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            add_if_valid(r+dr, c+dc)

    elif ptype == 'B':
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            x, y = r+dr, c+dc
            while in_bounds(x, y):
                target = board[x][y]
                if target == '.':
                    moves.append((x, y))
                elif piece_color(target) != color:
                    moves.append((x, y))
                    break
                else:
                    break
                x += dr; y += dc

    elif ptype == 'R':
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            x, y = r+dr, c+dc
            while in_bounds(x, y):
                target = board[x][y]
                if target == '.':
                    moves.append((x, y))
                elif piece_color(target) != color:
                    moves.append((x, y))
                    break
                else:
                    break
                x += dr; y += dc

    elif ptype == 'Q':
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]:
            x, y = r+dr, c+dc
            while in_bounds(x, y):
                target = board[x][y]
                if target == '.':
                    moves.append((x, y))
                elif piece_color(target) != color:
                    moves.append((x, y))
                    break
                else:
                    break
                x += dr; y += dc

    elif ptype == 'K':
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            add_if_valid(r+dr, c+dc)
        # Castling
        if castling_rights:
            back_row = 7 if color == 'w' else 0
            if r == back_row and c == 4:
                # Kingside
                ks_key = color + 'K'
                if castling_rights.get(ks_key) and board[back_row][5] == '.' and board[back_row][6] == '.':
                    if not is_square_attacked(board, back_row, 4, color) and \
                       not is_square_attacked(board, back_row, 5, color) and \
                       not is_square_attacked(board, back_row, 6, color):
                        moves.append((back_row, 6))
                # Queenside
                qs_key = color + 'Q'
                if castling_rights.get(qs_key) and board[back_row][3] == '.' and \
                   board[back_row][2] == '.' and board[back_row][1] == '.':
                    if not is_square_attacked(board, back_row, 4, color) and \
                       not is_square_attacked(board, back_row, 3, color) and \
                       not is_square_attacked(board, back_row, 2, color):
                        moves.append((back_row, 2))

    return moves

def is_square_attacked(board, r, c, by_color_of_defender):
    # Check if square (r,c) is attacked by opponent of by_color_of_defender
    attacker_color = 'b' if by_color_of_defender == 'w' else 'w'
    for ar in range(8):
        for ac in range(8):
            if board[ar][ac] != '.' and piece_color(board[ar][ac]) == attacker_color:
                # Don't pass castling rights here to avoid recursion
                raw_moves = get_valid_moves(board, ar, ac)
                if (r, c) in raw_moves:
                    return True
    return False

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] == color + 'K':
                return (r, c)
    return None

def is_in_check(board, color):
    king_pos = find_king(board, color)
    if king_pos is None:
        return False
    return is_square_attacked(board, king_pos[0], king_pos[1], color)

def make_move(board, fr, fc, tr, tc, en_passant_target=None, castling_rights=None):
    new_board = [row[:] for row in board]
    piece = new_board[fr][fc]
    color = piece[0]
    ptype = piece[1]
    new_ep = None
    new_cr = dict(castling_rights) if castling_rights else {}

    # En passant capture
    if ptype == 'P' and en_passant_target == (tr, tc):
        capture_row = fr  # the captured pawn is on the same row as moving pawn
        new_board[capture_row][tc] = '.'

    # Pawn double push sets en passant target
    if ptype == 'P' and abs(tr - fr) == 2:
        new_ep = ((fr + tr) // 2, tc)

    # Castling move
    if ptype == 'K' and abs(tc - fc) == 2:
        back_row = 7 if color == 'w' else 0
        if tc == 6:  # kingside
            new_board[back_row][5] = new_board[back_row][7]
            new_board[back_row][7] = '.'
        elif tc == 2:  # queenside
            new_board[back_row][3] = new_board[back_row][0]
            new_board[back_row][0] = '.'

    # Update castling rights
    if ptype == 'K':
        new_cr[color + 'K'] = False
        new_cr[color + 'Q'] = False
    if ptype == 'R':
        if fc == 7: new_cr[color + 'K'] = False
        if fc == 0: new_cr[color + 'Q'] = False

    new_board[tr][tc] = piece
    new_board[fr][fc] = '.'

    # Pawn promotion
    if ptype == 'P' and (tr == 0 or tr == 7):
        new_board[tr][tc] = color + 'Q'  # auto-promote to queen

    return new_board, new_ep, new_cr

def get_all_legal_moves(board, color, en_passant_target, castling_rights):
    legal = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != '.' and piece_color(board[r][c]) == color:
                raw = get_valid_moves(board, r, c, en_passant_target, castling_rights)
                for tr, tc in raw:
                    new_b, _, _ = make_move(board, r, c, tr, tc, en_passant_target, castling_rights)
                    if not is_in_check(new_b, color):
                        legal.append((r, c, tr, tc))
    return legal

def main():
    board = initial_board()
    turn = 'w'
    en_passant_target = None
    castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
    selected = None
    valid_moves = []
    move_history = []
    message = "White to move. Enter a square to select a piece (e.g. e2)"

    while True:
        print_board(board, selected, valid_moves)
        in_check = is_in_check(board, turn)
        color_name = "White" if turn == 'w' else "Black"
        if in_check:
            print(f"  ⚠️  {color_name} is in CHECK!")

        all_legal = get_all_legal_moves(board, turn, en_passant_target, castling_rights)
        if not all_legal:
            if in_check:
                winner = "Black" if turn == 'w' else "White"
                print(f"\n  ♚ CHECKMATE! {winner} wins!\n")
            else:
                print(f"\n  ½ STALEMATE! It's a draw.\n")
            input("  Press Enter to exit...")
            break

        print(f"  {message}")
        if move_history:
            last = move_history[-1]
            print(f"  Last move: {last}")
        print(f"  Turn: {color_name}  |  Commands: [square] to select/move, 'quit' to exit\n")

        try:
            user_input = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if user_input == 'quit' or user_input == 'q':
            print("\n  Thanks for playing!")
            break

        pos = parse_pos(user_input)
        if pos is None:
            message = "Invalid input. Enter a square like 'e2' or 'quit'."
            continue

        r, c = pos

        if selected is None:
            # Select a piece
            if board[r][c] == '.' or piece_color(board[r][c]) != turn:
                message = "No valid piece there. Select one of your pieces."
                continue
            raw_moves = get_valid_moves(board, r, c, en_passant_target, castling_rights)
            legal_dests = []
            for tr, tc in raw_moves:
                new_b, _, _ = make_move(board, r, c, tr, tc, en_passant_target, castling_rights)
                if not is_in_check(new_b, turn):
                    legal_dests.append((tr, tc))
            if not legal_dests:
                message = "That piece has no legal moves. Try another."
                continue
            selected = (r, c)
            valid_moves = legal_dests
            piece_str = PIECES.get(board[r][c], board[r][c])
            message = f"Selected {piece_str} at {pos_to_str(r,c)}. Now enter destination square."
        else:
            sr, sc = selected
            if (r, c) == selected:
                # Deselect
                selected = None
                valid_moves = []
                message = f"{color_name} to move. Select a piece."
            elif (r, c) in valid_moves:
                # Execute move
                from_str = pos_to_str(sr, sc)
                to_str = pos_to_str(r, c)
                new_board, new_ep, new_cr = make_move(board, sr, sc, r, c, en_passant_target, castling_rights)
                board = new_board
                en_passant_target = new_ep
                castling_rights = new_cr
                move_history.append(f"{from_str}→{to_str}")
                turn = 'b' if turn == 'w' else 'w'
                selected = None
                valid_moves = []
                next_color = "Black" if turn == 'b' else "White"
                message = f"{next_color} to move. Select a piece."
            else:
                # Maybe selecting a different piece
                if board[r][c] != '.' and piece_color(board[r][c]) == turn:
                    raw_moves = get_valid_moves(board, r, c, en_passant_target, castling_rights)
                    legal_dests = []
                    for tr, tc in raw_moves:
                        new_b, _, _ = make_move(board, r, c, tr, tc, en_passant_target, castling_rights)
                        if not is_in_check(new_b, turn):
                            legal_dests.append((tr, tc))
                    if legal_dests:
                        selected = (r, c)
                        valid_moves = legal_dests
                        piece_str = PIECES.get(board[r][c], board[r][c])
                        message = f"Selected {piece_str} at {pos_to_str(r,c)}. Enter destination."
                    else:
                        message = "That piece has no legal moves. Try another."
                else:
                    message = "Invalid destination. Try again or re-enter the piece square to deselect."

if __name__ == '__main__':
    main()
