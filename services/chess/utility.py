import re
from core.config import Config

def switch_side(side_turn):
    return Config.SIDE_BLACK if side_turn == Config.SIDE_WHITE else Config.SIDE_WHITE

def extract_square(move):
    match = re.findall(r"[a-h][1-8]", move)
    return match[-1] if match else move

def to_chess_notation(x, y):
    files = "abcdefgh"
    ranks = "12345678"

    return files[x-1] + ranks[y-1]

def chess_to_square(move):
    files = "abcdefgh"
    x = files.index(move[0]) + 1
    y = int(move[1])
    return (int(x), int(y))

def chess_to_square_flipped(move):
    files = "abcdefgh"
    x = 8 - files.index(move[0])
    y = 8 - int(move[1]) + 1
    return (int(x), int(y))

def parse_castling(move: str, side: str):
    move = move.replace("0", "O")  # just in case if 0-0

    if move == "O-O":
        if side == Config.SIDE_WHITE:
            return "e1", "g1"
        else:
            return "e8", "g8"

    if move == "O-O-O":
        if side == Config.SIDE_WHITE:
            return "e1", "c1"
        else:
            return "e8", "c8"

    return None

def parse_promotion(move: str):
    move = move.lower().strip().rstrip("+#")
    # check if it's promotion
    if "=" in move or move[-1] in "qrbn":
        move = move.replace("=", "")

        piece = move[-1]
        to_square = move[-3:-1]

        if piece in "qrbn":
            return to_square, piece

    return None, None

def chess_timer_to_seconds(t: str) -> int:
    parts = list(map(int, t.split(":")))

    if len(parts) == 2: #format MM:SS
        m, s = parts
        return m * 60 + s
    elif len(parts) == 3: #format H:MM:SS
        h, m, s = parts
        return h * 3600 + m * 60 + s