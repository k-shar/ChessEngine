import pygame
import random


class Bouncy():
    def __init__(self, screen_size, loc):

        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

        self.image = pygame.Surface([screen_size[0]//40] * 2)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = loc

    def update(self, size):
        self.rect.centerx += self.vx + random.randint(-1, 1)
        self.rect.centery += self.vy + random.randint(-1, 1)

        if self.rect.centerx >= size[0]:
            self.vx *= -1

        if self.rect.centery >= size[1]:
            self.vy *= -1

        if self.rect.centerx <= 0:
            self.vx *= -1

        if self.rect.centery <= 0:
            self.vy *= -1
