import pygame
from window_sizing import ScaleSurface


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
