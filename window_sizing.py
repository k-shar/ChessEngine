import pygame
from pygame import freetype


class ScaleSurface(pygame.sprite.Sprite):
    def __init__(self, color, ratio, alignment, padding):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        self.color = color
        self.ratio = ratio
        self.alignment = alignment
        self.padding = padding  # float 0-1 determining how much of the parent surf is filled

    def resize(self, parent):
        self.image.fill(self.color)

        # -- create padding between outer and inner --
        # create a shrunk outer surface to use instead, so when the inner surface is expanded there will be some gap
        shrunk_outer_surf = pygame.transform.scale(parent, (int(parent.get_width() * self.padding),
                                                            int(parent.get_height() * self.padding)))

        # -- expand to fill shrunk_outer_surf --
        max_size = list(shrunk_outer_surf.get_size())
        i = 0
        test_size = [self.ratio[0] * i, self.ratio[1] * i]
        # while test_size is not overflowing max_size, increase test_size
        while not(test_size[0] > max_size[0]) and not(test_size[1] > max_size[1]):
            i += 1  # increase the test size
            test_size = [self.ratio[0] * i, self.ratio[1] * i]

        # rollback last attempted scale up so we are no longer overflowing max_size
        test_size = [test_size[0] - self.ratio[0], test_size[1] - self.ratio[1]]
        # set image to the new scaled dimensions
        self.image = pygame.transform.scale(self.image, test_size)

        # -- center smaller surface --
        self.rect = self.image.get_rect()
        self.rect.centerx = int(parent.get_width() * self.alignment[0])
        self.rect.centery = int(parent.get_height() * self.alignment[1])


class TextSurface(ScaleSurface):
    def __init__(self, color, ratio, alignment, padding, text_color, text, text_size):
        super().__init__(color, ratio, alignment, padding)
        self.text_color = text_color
        self.text = text
        self.text_size = text_size

    def resize(self, parent):
        # resize the outer surface as normal
        super().resize(parent)

        # -- generate and blit text --
        font = pygame.freetype.SysFont("Consolas", self.image.get_height())
        if self.image.get_size() == (0, 0):  # first resize post will give a surface of dimensions 0
            self.text_surf, self.text_rect = font.render("this should only run once", fgcolor=self.text_color, size=1)
        else:
            self.text_surf, self.text_rect = font.render(self.text, fgcolor=self.text_color, size=self.image.get_height()*self.text_size)
        self.image.blit(self.text_surf, self.text_surf.get_rect(center=self.image.get_rect().center))


class Button(TextSurface):
    def __init__(self, color, ratio, alignment, padding, text_color, text, text_size, hover_color):
        super().__init__(color, ratio, alignment, padding, text_color, text, text_size)
        self.hover_color = hover_color

        self.hovered = False
        self.clicked = False

    def update(self, is_hovered):
        if is_hovered:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)

        self.image.blit(self.text_surf, self.text_surf.get_rect(center=self.image.get_rect().center))






