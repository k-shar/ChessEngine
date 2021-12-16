import pygame
from window_sizing import TextSurface
import engine_config


class Tile(TextSurface):
    def __init__(self, col, row, is_white):
        if is_white:
            color_name = "WHITE"
            font_color = "BLACK"
        else:
            color_name = "BLACK"
            font_color = "WHITE"

        self.coordinate = f"{chr(64 + col)}{row}"
        super().__init__(color_name, (1, 1), (col/8, row/8), 1/8, self.coordinate, 0.3, font_color, (0.4, 0.4))

    def resize(self, parent):
        super().resize(parent)
        # align the centers correctly
        # as ScaleSurface is center aligned, but the chess tiles are aligned by their top left corner
        self.rect.centerx = self.rect.x
        self.rect.centery = self.rect.y

    def update(self, chess_board):

        self.image = pygame.Surface((chess_board.get_rect().height//2, chess_board.get_rect().width//2))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

