import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, key):
        super().__init__()

        self.image = pygame.Surface((1, 1))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()


    def update(self, chess_board):

        self.image = pygame.Surface((chess_board.get_rect().height//2, chess_board.get_rect().width//2))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

