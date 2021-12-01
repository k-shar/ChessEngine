import pygame
from pygame import freetype


class ScaleWindow:
    def __init__(self, color, ratio, alignment, padding):
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.pos = (0, 0)

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

        self.image = expand_to_fill(self.image, shrunk_outer_surf, self.ratio)

        # -- center smaller surface --
        self.rect = self.image.get_rect()
        self.rect.centerx = int(parent.get_width() * self.alignment[0])
        self.rect.centery = int(parent.get_height() * self.alignment[1])


def expand_to_fill(smaller, larger, ratio):
    """returns a surface resized to fill the larger surface while maintaining the ratio"""
    maximum_size = list(larger.get_size())
    i = 0
    while True:
        i += 1
        # create a dummy list to hold the increased size
        test_size = [ratio[0] * i, ratio[1] * i]
        # check if size is too big to fit in the larger surface
        if test_size[0] > maximum_size[0] or test_size[1] > maximum_size[1]:
            # rollback last attempted scale up
            test_size = [test_size[0] - ratio[0], test_size[1] - ratio[1]]
            # scale smaller surface to new dimensions and return
            resized = pygame.transform.scale(smaller, test_size)
            return resized




def resize_text(shrink, surf, outer_surf, ratio, alignment):

    surf.fill((255, 10, 10))
    surf, surf_pos = resize_surface(shrink, surf, outer_surf, ratio, alignment)

    # -- generate and blit text --
    font = pygame.freetype.SysFont("bell", surf.get_height())
    if surf.get_size() == (0, 0):
        text_surf, text_rect = font.render("test", fgcolor=(255, 255, 255), size=60)
    else:
        text_surf, text_rect = font.render("test", fgcolor=(255, 255, 255), size=surf.get_height()*0.7)
    surf.blit(text_surf, text_surf.get_rect(center=surf.get_rect().center))

    return surf, surf_pos
