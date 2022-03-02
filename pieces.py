import pygame
from engine_config import knight_square_table, pawn_square_table, bishop_square_table, rook_square_table


class Piece():
    def __init__(self, file, tile_index, color):
        self.file = pygame.image.load(file)
        self.tile_index = tile_index
        self.selected = False
        self.color = color
        self.location_evaluation = 0

    def set_location_evaluation(self, tile_group):
        return tile_group[self.tile_index].pos

    def resize(self, rect, enlarge):
        self.parent = rect
        self.image = pygame.transform.scale(self.file, (int(rect[0] * enlarge), int(rect[1] * enlarge)))
        self.rect = self.image.get_rect()
        self.rect.centerx = rect[0] // 2
        self.rect.centery = rect[1] // 2

    def hover(self, hovered):
        if hovered:
            # self.file = pygame.image.load("img/black_rook.svg")
            self.resize(self.parent, 1.1)
        else:
            self.resize(self.parent, 1)

    def generate_legal_moves(self, tile_group, piece_group):
        print("dont be here")
        return [self.tile_index, 24, 45, 34]


def generate_orthogonal_moves(tile_index, tile_group, color, piece_group):
    friendly_pieces = []
    enemy_pieces = []
    for piece in piece_group:  # extract the location of the pieces
        if piece.color == color:
            friendly_pieces.append(piece.tile_index)
        else:
            enemy_pieces.append(piece.tile_index)
    pieces_on_these_indices = friendly_pieces + enemy_pieces
    pieces_on_these_indices.remove(tile_index)

    legal_moves = [tile_index]  # always return the pieces origonal square as a legal move

    # left row
    index = tile_index
    while index % 8 != 0 and index not in pieces_on_these_indices:  # halt when hitting the right side of the board
        legal_moves.append(index)
        index -= 1  # -1 moves the index pointer to the left square
    if index in pieces_on_these_indices:  # a piece has been hit
        if index in enemy_pieces:
            legal_moves.append(index)  # its legal to capture an enemy piece
    else:
        legal_moves.append(index)

    # right row
    index = tile_index + 1
    while index % 8 != 0 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index += 1
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)

    # up column
    index = tile_index
    while index > 7 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index -= 8
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    # down column
    index = tile_index
    while index < 56 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index += 8
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    return legal_moves


def generate_diagonal_moves(tile_index, tile_group, color, piece_group):
    friendly_pieces = []
    enemy_pieces = []
    for piece in piece_group:
        if piece.color == color:
            friendly_pieces.append(piece.tile_index)
        else:
            enemy_pieces.append(piece.tile_index)
    pieces_on_these_indices = friendly_pieces + enemy_pieces
    pieces_on_these_indices.remove(tile_index)

    legal_moves = [tile_index]

    # top left diagonal
    index = tile_index
    while index % 8 != 0 and index > 7 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index -= 9
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    # top right diagonal
    index = tile_index
    while (index + 1) % 8 != 0 and index > 7 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index -= 7
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    # bottom left diagonal
    index = tile_index
    while index % 8 != 0 and index < 56 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index += 7
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    # bottom right diagonal
    index = tile_index
    while (index + 1) % 8 != 0 and index < 56 and index not in pieces_on_these_indices:
        legal_moves.append(index)
        index += 9
    if index in pieces_on_these_indices:
        if index in enemy_pieces:
            legal_moves.append(index)
    else:
        legal_moves.append(index)

    return legal_moves


class Pawn(Piece):
    def __init__(self, color, tile_index):
        self.color = color

        if self.color == "black":
            self.name = "p"
            super().__init__("img/black_pawn.svg", tile_index, color)
        if self.color == "white":
            self.name = "P"
            super().__init__("img/white_pawn.svg", tile_index, color)

    def set_location_evaluation(self, tile_group):
        coord = super().set_location_evaluation(tile_group)
        if self.color == "white":
            self.location_evaluation = pawn_square_table[coord[1]-1][coord[0]-1]
        else:
            self.location_evaluation = pawn_square_table[8 - coord[1]][coord[0] - 1]
        self.location_evaluation *= 2

    def generate_legal_moves(self, tile_group, piece_group):
        pieces_on_these_indices = []
        for piece in piece_group:
            pieces_on_these_indices.append(piece.tile_index)
        pieces_on_these_indices.remove(self.tile_index)

        legal_moves = [self.tile_index]
        if self.color == "white":
            # check for pawn captures
            if self.tile_index - 7 in pieces_on_these_indices or self.tile_index - 9 in pieces_on_these_indices:
                for piece in piece_group:
                    if (piece.tile_index == self.tile_index - 7 or piece.tile_index == self.tile_index - 9) and \
                            piece.color != self.color:
                        legal_moves.append(piece.tile_index)

            # if on back rank
            if 0 <= self.tile_index <= 7:
                print("time to queen")  # TODO: pawn promotion
                return [self.tile_index]
                # check whats blocking
            # home rank can move double
            elif 47 < self.tile_index < 56 and self.tile_index - 16 not in pieces_on_these_indices \
                    and self.tile_index - 8 not in pieces_on_these_indices:
                # move two squares if on home rank (and nothihng blocking)
                return legal_moves + [self.tile_index - 8, self.tile_index - 16]
            elif self.tile_index - 8 in pieces_on_these_indices:
                return legal_moves
            else:
                return legal_moves + [self.tile_index, self.tile_index - 8]

        # for a black pawn
        else:
            # check for pawn captures
            if self.tile_index + 7 in pieces_on_these_indices or self.tile_index + 9 in pieces_on_these_indices:
                for piece in piece_group:
                    if (piece.tile_index == self.tile_index + 7 or piece.tile_index == self.tile_index + 9) and \
                            piece.color != self.color:
                        legal_moves.append(piece.tile_index)

            # if on back rank
            if 56 <= self.tile_index <= 65:
                print("time to queen")  # TODO: pawn promotion
                return [self.tile_index]

            # check whats blocking
            # home rank can move double
            elif 7 < self.tile_index < 16 and self.tile_index + 16 not in pieces_on_these_indices \
                    and self.tile_index + 8 not in pieces_on_these_indices:
                # move two squares if on home rank (and nothihng blocking)
                return legal_moves + [self.tile_index + 8, self.tile_index + 16]
            elif self.tile_index + 8 in pieces_on_these_indices:
                return legal_moves
            else:
                return legal_moves + [self.tile_index + 8]


class Rook(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "r"
            super().__init__("img/black_rook.svg", tile_index, color)
        if self.color == "white":
            self.name = "R"
            super().__init__("img/white_rook.svg", tile_index, color)

    def set_location_evaluation(self, tile_group):
        coord = super().set_location_evaluation(tile_group)
        if self.color == "white":
            self.location_evaluation = rook_square_table[coord[1]-1][coord[0]-1]
        else:
            self.location_evaluation = rook_square_table[8 - coord[1]][coord[0] - 1]

    def generate_legal_moves(self, tile_group, piece_group):
        return generate_orthogonal_moves(self.tile_index, tile_group, self.color, piece_group)


class Knight(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "n"
            super().__init__("img/black_knight.svg", tile_index, color)
        if self.color == "white":
            self.name = "N"
            super().__init__("img/white_knight.svg", tile_index, color)
        self.location_evaluation = 0

    def set_location_evaluation(self, tile_group):
        coord = super().set_location_evaluation(tile_group)
        if self.color == "white":
            self.location_evaluation = knight_square_table[coord[1]-1][coord[0]-1]
        else:
            self.location_evaluation = knight_square_table[8 - coord[1]][coord[0] - 1]



    def generate_legal_moves(self, tile_list, piece_group):
        friendly_pieces = []
        for piece in piece_group:
            if piece.color == self.color:
                friendly_pieces.append(piece.tile_index)
        friendly_pieces.remove(self.tile_index)

        legal_moves = [self.tile_index]
        coordinate = tile_list[self.tile_index].pos
        # top left
        if coordinate[0] > 1 and coordinate[1] > 2 and (self.tile_index-17) not in friendly_pieces:
            legal_moves.append(self.tile_index - 17)
        # top right
        if coordinate[0] < 8 and coordinate[1] > 2 and (self.tile_index-15) not in friendly_pieces:
            legal_moves.append(self.tile_index - 15)
        # left top
        if coordinate[0] > 2 and coordinate[1] > 1 and (self.tile_index-10) not in friendly_pieces:
            legal_moves.append(self.tile_index - 10)
        # left bottom
        if coordinate[0] > 2 and coordinate[1] < 8 and (self.tile_index+6) not in friendly_pieces:
            legal_moves.append(self.tile_index + 6)
        # bottom left
        if coordinate[0] > 1 and coordinate[1] < 7 and (self.tile_index+15) not in friendly_pieces:
            legal_moves.append(self.tile_index + 15)
        # bottom right
        if coordinate[0] < 8 and coordinate[1] < 7 and (self.tile_index+17) not in friendly_pieces:
            legal_moves.append(self.tile_index + 17)
        # right bottom
        if coordinate[0] < 7 and coordinate[1] < 8 and (self.tile_index+10) not in friendly_pieces:
            legal_moves.append(self.tile_index + 10)
        # right top
        if coordinate[0] < 7 and coordinate[1] > 1 and (self.tile_index-6) not in friendly_pieces:
            legal_moves.append(self.tile_index - 6)

        return legal_moves


class Bishop(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "b"
            super().__init__("img/black_bishop.svg", tile_index, color)
        if self.color == "white":
            self.name = "B"
            super().__init__("img/white_bishop.svg", tile_index, color)

    def set_location_evaluation(self, tile_group):
        coord = super().set_location_evaluation(tile_group)
        if self.color == "white":
            self.location_evaluation = bishop_square_table[coord[1]-1][coord[0]-1]
        else:
            self.location_evaluation = bishop_square_table[8 - coord[1]][coord[0] - 1]

    def generate_legal_moves(self, tile_group, piece_group):
        return generate_diagonal_moves(self.tile_index, tile_group, self.color, piece_group)


class King(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "k"
            super().__init__("img/black_king.svg", tile_index, color)
        if self.color == "white":
            self.name = "K"
            super().__init__("img/white_king.svg", tile_index, color)

    def generate_legal_moves(self, tile_group, piece_group):
        friendly_pieces = []
        for piece in piece_group:
            if piece.color == self.color:
                friendly_pieces.append(piece.tile_index)
        friendly_pieces.remove(self.tile_index)

        index = self.tile_index
        coordinate = tile_group[self.tile_index].pos
        legal_moves = [index]

        # variables for diagonals
        # up-left, up-right, down-left, down-right
        ul, ur, dl, dr = True, True, True, True

        # orthogonal directions, and decide if diagonals are legal
        if coordinate[0] != 8:
            if (index+1) not in friendly_pieces:
                legal_moves.append(index + 1)  # left
        else:
            ur, dr = False, False

        if coordinate[0] != 1:
            if (index-1) not in friendly_pieces:
                legal_moves.append(index - 1)  # right
        else:
            ul, dl = False, False

        if coordinate[1] != 1:
            if (index-8) not in friendly_pieces:
                legal_moves.append(index - 8)  # up
        else:
            ul, ur = False, False

        if coordinate[1] != 8:
            if (index+8) not in friendly_pieces:
                legal_moves.append(index + 8)  # down
        else:
            dl, dr = False, False

        # diagonals
        if ul:
            if (index-9) not in friendly_pieces:
                legal_moves.append(index - 9)
        if ur:
            if (index-7) not in friendly_pieces:
                legal_moves.append(index - 7)
        if dl:
            if (index+7) not in friendly_pieces:
                legal_moves.append(index + 7)
        if dr:
            if (index+9) not in friendly_pieces:
                legal_moves.append(index + 9)

        return legal_moves


class Queen(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "q"
            super().__init__("img/black_queen.svg", tile_index, color)
        if self.color == "white":
            self.name = "Q"
            super().__init__("img/white_queen.svg", tile_index, color)

    def generate_legal_moves(self, tile_group, piece_group):
        return generate_diagonal_moves(self.tile_index, tile_group, self.color, piece_group) + \
               generate_orthogonal_moves(self.tile_index, tile_group, self.color, piece_group)
