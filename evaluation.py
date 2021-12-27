from math import e
from random import randint
import matplotlib.pyplot as plt
from engine_config import piece_values
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


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

    return evaluation


def static_evaluation(piece_group):
    return round(relative_piece_sum(piece_group), 4)


def minimax(input_piece_group, tile_group, depth, maximising):

    maximising = True
    if depth == 0:  # TODO: add game over
        return static_evaluation(input_piece_group)

    # if we are trying to maximise the evaluation
    if maximising:
        current_move_evaluation = -999
        best_move = None
        best_evaluation = -999

        for i in range(len(input_piece_group)):
            if input_piece_group[i].color == "black":  # only move the friendly pieces
                for move in input_piece_group[i].generate_legal_moves(tile_group, input_piece_group):

                    # test this move by playing it
                    analysis_piece_group = input_piece_group.copy()
                    analysis_piece_group[i].tile_index = move
                    current_move_evaluation = minimax(analysis_piece_group, tile_group, depth - 1, False) # TODO: make move on fen
                    print(move)
                    if current_move_evaluation > best_evaluation:
                        best_evaluation = current_move_evaluation
                        best_move = input_piece_group[i], move

    print(best_evaluation, best_move)


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
