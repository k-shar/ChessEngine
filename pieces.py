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
    def __init__(self, file, tile_index):
        self.file = pygame.image.load(file)
        self.tile_index = tile_index
        self.selected = False

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


class Pawn(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_pawn.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_pawn.svg", tile_index)


class Rook(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_rook.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_rook.svg", tile_index)


class Knight(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_knight.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_knight.svg", tile_index)


class Bishop(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_bishop.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_bishop.svg", tile_index)


class King(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_king.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_king.svg", tile_index)


class Queen(Piece):
    def __init__(self, color, tile_index):
        self.color = color
        if self.color == "black":
            super().__init__("img/black_queen.svg", tile_index)
        if self.color == "white":
            super().__init__("img/white_queen.svg", tile_index)
