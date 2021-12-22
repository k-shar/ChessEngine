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

    def generate_legal_moves(self):
        return [self.tile_index, 24, 45, 34]

class Pawn(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        self.already_moved = False

        if self.color == "black":
            self.name = "p"
            super().__init__("img/black_pawn.svg", tile_index, color)
        if self.color == "white":
            self.name = "P"
            super().__init__("img/white_pawn.svg", tile_index, color)

    def generate_legal_moves(self):
        if self.color == "white":
            if self.already_moved:
                return [self.tile_index, self.tile_index - 8]
            else:
                return [self.tile_index, self.tile_index - 8, self.tile_index - 16]
        else:
            if self.already_moved:
                return [self.tile_index, self.tile_index + 8]
            else:
                return [self.tile_index, self.tile_index + 8, self.tile_index + 16]

class Rook(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "r"
            super().__init__("img/black_rook.svg", tile_index, color)
        if self.color == "white":
            self.name = "R"
            super().__init__("img/white_rook.svg", tile_index, color)


class Knight(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "n"
            super().__init__("img/black_knight.svg", tile_index, color)
        if self.color == "white":
            self.name = "N"
            super().__init__("img/white_knight.svg", tile_index, color)


class Bishop(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "b"
            super().__init__("img/black_bishop.svg", tile_index, color)
        if self.color == "white":
            self.name = "B"
            super().__init__("img/white_bishop.svg", tile_index, color)


class King(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "k"
            super().__init__("img/black_king.svg", tile_index, color)
        if self.color == "white":
            self.name = "K"
            super().__init__("img/white_king.svg", tile_index, color)


class Queen(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            self.name = "q"
            super().__init__("img/black_queen.svg", tile_index, color)
        if self.color == "white":
            self.name = "Q"
            super().__init__("img/white_queen.svg", tile_index, color)
