def is_valid_fen(FEN):

    # split the FEN into its component parts for testing individually
    FEN = FEN.split()

    # -- check piece position is valid --
    piece_position = FEN[0].split("/")

    # check that there are enough rows
    if len(piece_position) != 8:
        raise Exception(f"There are {len(piece_position)} rows in the given FEN (should be 8)")

    # check there are enough columns in each row
    # and that each item in the row is valid
    for row in piece_position:
        total_columns = 0
        for item in row:
            if item in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                total_columns += int(item)
            elif item.lower() in ["p", "r", "n", "b", "q", "k"]:
                total_columns += 1
            else:
                raise Exception(f"Item '{item}' is not a valid piece name/ empty square count")
        if total_columns != 8:
            raise Exception(f"Row '{row}' does has {total_columns} columns worth of information (should be 8)")

    # -- check active color is valid --
    active_color = FEN[1]
    if active_color not in ["w", "b"]:
        raise Exception(f"Invalid active color '{active_color}' is not valid (should be 'w' or 'b')")

    # -- check castling rights are valid --
    legal = True
    castling_rights = FEN[2]
    if castling_rights[0] not in ["K", "-"]: legal = False
    if castling_rights[1] not in ["Q", "-"]: legal = False
    if castling_rights[2] not in ["k", "-"]: legal = False
    if castling_rights[3] not in ["q", "-"]: legal = False
    if not legal:
        raise Exception(f"Invalid castling rights '{castling_rights}'")

    return True


def make_move_on_FEN(fen, move, previous_square):
    split_fen = fen.split(" ")
    rows = fen.split(" ")[0].split("/")

    # set piece on new square
    column_of_new_row = list(rows[move[2][1] - 1])
    column_of_new_row[move[2][0] - 1] = move[0]  # set piece
    rows[move[2][1] - 1] = "".join(column_of_new_row)  # set the move to the rows

    # set old square as empty
    column_of_old_row = list(rows[previous_square[1] - 1])
    column_of_old_row[previous_square[0] - 1] = "1"
    rows[previous_square[1] - 1] = "".join(column_of_old_row)

    new_fen = ""
    for row in rows:
        new_fen += row + "/"
    new_fen = new_fen[:-1]
    for component in split_fen[1:]:
        new_fen += " " + component

    is_valid_fen(new_fen)
    return new_fen


if __name__ == "__main__":
    # unit test cases
    print(is_valid_fen("rnbqkbnr/ppppppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"))
    print(is_valid_fen("pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"))
    print(is_valid_fen("rnbqkbnX/ppppPpppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"))
    print(is_valid_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR G KQkq"))
    print(is_valid_fen("2p2p2/8/7p/8/8/4p3/8/8 w KQkq"))
    print(is_valid_fen("8/8/8/8/8/8/8/8 w --XX"))
