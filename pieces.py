import pygame
from window_sizing import ScaleSurface

def instasiate_pieces(FEN):

    fen = FEN.split(" ")[0].split("/")[:8]

    piece_group = []
    tile_index = 0
    for row in fen:
        for item in row:
            if item == "p": piece_group.append(Pawn("black", tile_index))
            elif item == "P": piece_group.append(Pawn("white", tile_index))
            elif item == "r": piece_group.append(Rook("black", tile_index))
            elif item == "R": piece_group.append(Rook("white", tile_index))
            elif item == "n": piece_group.append(Knight("black", tile_index))
            elif item == "N": piece_group.append(Knight("white", tile_index))
            elif item == "b": piece_group.append(Bishop("black", tile_index))
            elif item == "B": piece_group.append(Bishop("white", tile_index))
            elif item == "k": piece_group.append(King("black", tile_index))
            elif item == "K": piece_group.append(King("white", tile_index))
            elif item == "q": piece_group.append(Queen("black", tile_index))
            elif item == "Q": piece_group.append(Queen("white", tile_index))

            else:
                tile_index += int(item)-1
            tile_index += 1
    return piece_group


class Piece():
    def __init__(self, file, tile_index, color):
        self.file = pygame.image.load(file)
        self.tile_index = tile_index
        self.selected = False
        self.color = color

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

    def generate_legal_moves(self, tile_group):
        print("dont be here")
        return [self.tile_index, 24, 45, 34]

def generate_orthogonal_moves(tile_index, tile_group):
    legal_moves = [tile_index]

    # left row
    index = tile_index
    while index % 8 != 0:
        legal_moves.append(index)
        index -= 1
    legal_moves.append(index)

    # right row
    index = tile_index + 1
    while index % 8 != 0:
        legal_moves.append(index)
        index += 1

    # up column
    index = tile_index
    while index > 7:
        legal_moves.append(index)
        index -= 8
    legal_moves.append(index)

    # down column
    index = tile_index
    while index < 56:
        legal_moves.append(index)
        index += 8
    legal_moves.append(index)

    return legal_moves


def generate_diagonal_moves(tile_index, tile_group):
    legal_moves = [tile_index]

    # top left diagonal
    index = tile_index
    while index % 8 != 0 and index > 7:
        legal_moves.append(index)
        index -= 9
    legal_moves.append(index)

    # top right diagonal
    index = tile_index
    while (index+1) % 8 != 0 and index > 7:
        index -= 7
        legal_moves.append(index)

    # bottom left diagonal
    index = tile_index
    while index % 8 != 0 and index < 56:
        legal_moves.append(index)
        index += 7
    legal_moves.append(index)

    # bottom right diagonal
    index = tile_index
    while (index+1) % 8 != 0 and index < 56:
        legal_moves.append(index)
        index += 9
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

    def generate_legal_moves(self, tile_group):
        if self.color == "white":
            if 47 < self.tile_index < 56:  # home rank can move double
                return [self.tile_index, self.tile_index - 8, self.tile_index - 16]
            else:
                if 0 <= self.tile_index <= 7:
                    print("time to queen")  # TODO: pawn promotion
                    return [self.tile_index]
                return [self.tile_index, self.tile_index - 8]
        else:
            if 7 < self.tile_index < 16:  # home rank can move double
                return [self.tile_index, self.tile_index + 8, self.tile_index + 16]
            else:
                if 56 <= self.tile_index <= 65:
                    print("time to queen")  # TODO: pawn promotion
                    return [self.tile_index]
                return [self.tile_index, self.tile_index + 8]

class Rook(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "r"
            super().__init__("img/black_rook.svg", tile_index, color)
        if self.color == "white":
            self.name = "R"
            super().__init__("img/white_rook.svg", tile_index, color)

    def generate_legal_moves(self, tile_group):
        return generate_orthogonal_moves(self.tile_index, tile_group)


class Knight(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "n"
            super().__init__("img/black_knight.svg", tile_index, color)
        if self.color == "white":
            self.name = "N"
            super().__init__("img/white_knight.svg", tile_index, color)

    def generate_legal_moves(self, tile_list):
        legal_moves = [self.tile_index]
        coordinate = tile_list[self.tile_index].pos
        # top left
        if coordinate[0] > 1 and coordinate[1] > 2:
            legal_moves.append(self.tile_index - 17)
        # top right
        if coordinate[0] < 8 and coordinate[1] > 2:
            legal_moves.append(self.tile_index - 15)
        # left top
        if coordinate[0] > 2 and coordinate[1] > 1:
            legal_moves.append(self.tile_index - 10)
        # left bottom
        if coordinate[0] > 2 and coordinate[1] < 8:
            legal_moves.append(self.tile_index + 6)
        # bottom left
        if coordinate[0] > 1 and coordinate[1] < 7:
            legal_moves.append(self.tile_index + 15)
        # bottom right
        if coordinate[0] < 8 and coordinate[1] < 7:
            legal_moves.append(self.tile_index + 17)
        # right bottom
        if coordinate[0] < 7 and coordinate[1] < 8:
            legal_moves.append(self.tile_index + 10)
        # right top
        if coordinate[0] < 7 and coordinate[1] > 1:
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

    def generate_legal_moves(self, tile_group):
        return generate_diagonal_moves(self.tile_index, tile_group)


class King(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "k"
            super().__init__("img/black_king.svg", tile_index, color)
        if self.color == "white":
            self.name = "K"
            super().__init__("img/white_king.svg", tile_index, color)

    def generate_legal_moves(self, tile_group):
        index = self.tile_index
        return [index, index+1, index+7, index+8, index+9, index-1, index-7, index-8, index-9]

class Queen(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "q"
            super().__init__("img/black_queen.svg", tile_index, color)
        if self.color == "white":
            self.name = "Q"
            super().__init__("img/white_queen.svg", tile_index, color)

    def generate_legal_moves(self, tile_group):
        return generate_diagonal_moves(self.tile_index, tile_group) + generate_orthogonal_moves(self.tile_index, tile_group)