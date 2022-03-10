from math import e
from random import randint
import matplotlib.pyplot as plt
from engine_config import piece_values
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from fen_manipulation import instasiate_pieces, make_move_on_FEN
from threading import Thread


def normalise_evaluation(eval):
    scale = 0.4
    tanhx = ((e**(scale * eval) - 1)/(e**(scale * eval) + 1))
    return (tanhx + 1) / 2


def generate_evaluation_spectrum(start, end):
    spectrum = []
    N = 50
    for i in range(N):
        spectrum.append(start + (end-start)*i/N)
    spectrum.reverse()
    return spectrum


def relative_piece_sum(piece_group):
    evaluation = 0
    # polarity to decide weather the piece adds or subtracts from the evaluation
    for piece in piece_group:
        if piece.color == "white":
            polarity = -1
        elif piece.color == "black":
            polarity = 1
        else:
            raise Exception(f"'{piece.color}' is not black or white")

        if type(piece) is Pawn:
            evaluation += polarity * piece_values["pawn"]
        elif type(piece) is Rook:
            evaluation += polarity * piece_values["rook"]
        elif type(piece) is Knight:
            evaluation += polarity * piece_values["knight"]
        elif type(piece) is Bishop:
            evaluation += polarity * piece_values["bishop"]
        elif type(piece) is Queen:
            evaluation += polarity * piece_values["queen"]
        elif type(piece) is King:
            evaluation += polarity * piece_values["king"]

    return evaluation


def piece_square_tables(piece_group):
    eval = 0
    for piece in piece_group:
        if piece.color == "white":
            eval -= piece.location_evaluation
        else:
            eval += piece.location_evaluation
    return eval


def static_evaluation(piece_group):
    evaluation = relative_piece_sum(piece_group) + piece_square_tables(piece_group)
    return round(evaluation, 4)


def alphabeta(FEN, tile_group, depth, maximising, alpha, beta):
    piece_group = instasiate_pieces(FEN)

    if depth == 0:  # TODO: add game over
        for piece in piece_group:
            piece.set_location_evaluation(tile_group)  # update its location evaluation

        return FEN, static_evaluation(piece_group)

    if maximising:
        best_move = None
        best_evaluation = -9999999

        for i in range(len(piece_group)-1):
            if piece_group[i].color == "black":  # only move the friendly pieces
                for move in piece_group[i].generate_legal_moves(tile_group, piece_group):
                    if move != piece_group[i].tile_index:
                        # play this move
                        for tile in tile_group:
                            if tile.tile_index == piece_group[i].tile_index:
                                old_tile = tile
                            elif tile.tile_index == move:
                                new_tile = tile
                        move = piece_group[i].name, new_tile.coordinate, new_tile.pos
                        new_fen = make_move_on_FEN(FEN, move, old_tile.pos)

                        # evaluate move
                        current_move_evaluation = alphabeta(new_fen, tile_group, depth - 1, False, alpha, beta)[1]

                        # print(piece_group[i], piece_group[i].color, move, current_move_evaluation, best_evaluation)

                        if current_move_evaluation >= best_evaluation:
                            # bishop is 0.2, should be -3
                            best_evaluation = current_move_evaluation
                            best_move = new_fen, move

                        if best_move is None:
                            best_move = new_fen, move

                        alpha = max(alpha, best_evaluation)
                        if best_evaluation >= beta:
                            break
        try:
            return best_move[0], best_evaluation
        except:
            return None, best_evaluation

    # minimising case
    else:
        best_move = None
        best_evaluation = 99999999

        for i in range(len(piece_group)-1):
            if piece_group[i].color == "white":  # only move the friendly pieces
                for move in piece_group[i].generate_legal_moves(tile_group, piece_group):
                    if move != piece_group[i].tile_index:

                        # play this move
                        for tile in tile_group:
                            if tile.tile_index == piece_group[i].tile_index:
                                old_tile = tile
                            elif tile.tile_index == move:
                                new_tile = tile
                        move = piece_group[i].name, new_tile.coordinate, new_tile.pos
                        new_fen = make_move_on_FEN(FEN, move, old_tile.pos)

                        # evaluate move
                        current_move_evaluation = alphabeta(new_fen, tile_group, depth - 1, True, alpha, beta)[1]

                        # print(move, piece_group[i], current_move_evaluation, depth)
                        # print(piece_group[i], piece_group[i].color, move, current_move_evaluation, best_evaluation)

                        if current_move_evaluation <= best_evaluation:
                            best_evaluation = current_move_evaluation
                            best_move = new_fen, move

                        if best_move is None:
                            best_move = new_fen, move

                        beta = min(beta, best_evaluation)
                        if best_evaluation <= alpha:
                            break

        try:
            return best_move[0], best_evaluation
        except:
            return None, best_evaluation


if __name__ == "__main__":
    infinity = 15

    input_evaluations = []
    for i in range(100):
        input_evaluations.append(randint(-infinity, infinity))

    evaluation_slider_center = []
    for input in input_evaluations:
        print(input)
        evaluation_slider_center.append(normalise_evaluation(input))

    plt.plot(input_evaluations, evaluation_slider_center, "x")
    plt.show()

    print(generate_evaluation_spectrum(5, 50))
