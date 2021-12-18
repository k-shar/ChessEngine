import pygame
from window_sizing import TextSurface
import engine_config


class Tile(TextSurface):
    def __init__(self, col, row, is_white, tile_index):
        if is_white:
            color_name = "WHITE"
            font_color = "BLACK"
        else:
            color_name = "BLACK"
            font_color = "WHITE"
        self.pos = [col, row]
        self.tile_index = tile_index

        # self.coordinate = str(tile_index)
        self.coordinate = f"{chr(64 + col)}{9 - row}"
        super().__init__(color_name, (1, 1), (col/8, row/8), 1/8, self.coordinate, 0.3, font_color, (0.4, 0.4))

    def setcolor(self, color):
        self.text_color = (255, 0, 0)

    def resize(self, parent):
        super().resize(parent)
        # align the centers correctly
        # as ScaleSurface is center aligned, but the chess tiles are aligned by their top left corner
        self.rect.centerx = self.rect.x
        self.rect.centery = self.rect.y