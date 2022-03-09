import random

puzzles = [
    "111k1111/R111111p/11p1p1pq/11111111/1111N11p/1111PP11/1111K11p/11111111 w KQkq",
    "1k11111r/pP111ppp/111p11b1/1BN1n111/1Q11P111/P1B11111/KP111P1P/1111111q w ----",
    "r11qk11r/pb1111pp/1n11Pb11/11B11Q11/p1p11111/11P11111/11B11PPP/RN11R1K1 w ----"
    ]

endgames = [
    "1111k111/11111111/11111111/1111p111/11111111/11111111/11111K11/11111Q11 w KQkq",
    "1k111111/11111111/11111111/11111111/11111111/11111111/111KR111/11111111 w KQkq",
    "11k11111/11111111/11111111/1111111P/11111111/11111111/1K1111R1/11111111 w KQkq",
    "111111k1/11111111/11111111/11111111/11111111/11111111/111K1111/1R111111 w KQkq",
    "1111k111/11111111/11111111/11111111/11111111/11111R11/111K1111/11111111 w KQkq",
    "111k1111/11111111/pp111111/11111111/R1111111/11111111/111KR111/11111111 w KQkq",
    "11k11111/11111111/11111111/P1111111/11111111/11111111/111KR111/11111111 w KQkq",
    "11111111/1k111111/1111p111/11111111/11111111/111111R1/111Kn111/11111111 w KQkq",
    "11111111/1111k111/11111111/1111Pb11/111PP111/11111111/111K1111/1R111111 w KQkq",
    "11111111/11111k11/111n1111/11111111/11111111/11111R11/111K1111/11111111 w KQkq",
    "11111k11/1k111111/pp111111/11111111/1n111111/11111111/111KR111/11111111 w KQkq",
    "111k1111/1k111111/11111111/B1111111/11111111/11111111/111KR111/11111111 w KQkq",
    "111111k1/11111111/111111b1/11111111/11111111/111111R1/111Kn111/11111111 w KQkq",
    ]

def generate_random_fen():
    fen = []
    for row in range(8):
        row = ""
        for column in range(8):
            if random.randint(1, 10) == 3:
                row += random.choice(["r", "R", "N", "N", "P", "p", "B", "b"])
            else:
                row += "1"
        fen.append(row)

    # add kings
    white_king_riow = ""
    for column in range(8):
        if random.randint(1, 10) == 3:
            white_king_riow += random.choice(["r", "R", "N", "N", "P", "p", "B", "b"])
        else:
            white_king_riow += "1"
    white_king_riow = list(white_king_riow)
    white_king_riow[random.randint(0, 7)] = "k"
    white_king_riow = "".join(white_king_riow)
    fen[random.randint(0, 3)] = white_king_riow

    black_king_row = ""
    for column in range(8):
        if random.randint(1, 10) == 3:
            black_king_row += random.choice(["r", "R", "N", "N", "P", "p", "B", "b"])
        else:
            black_king_row += "1"
    black_king_row = list(black_king_row)
    black_king_row[random.randint(0, 7)] = "K"
    black_king_row = "".join(black_king_row)
    fen[random.randint(4, 7)] = black_king_row

    return "/".join(fen) + " w KQkq"
