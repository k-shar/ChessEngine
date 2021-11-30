import pygame
from pygame import freetype

def expand_fill_maintaining_ratio(smaller, larger, ratio):
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


def resize_surface(shrink, surf, outer_surf, ratio, alignment):

    # "shrink" is a float from 0-1 determining how much of the outer surface the inner will fill
    if (type(shrink) != float and shrink != 1) or not(0 < shrink <= 1):
        raise ValueError("shrink must be float between 0 and 1")

    # -- create padding between outer and inner --
    # create a shrunk outer surface to use instead, so when the inner surface is expanded there will be some gap
    shrunk_outer_surf = pygame.transform.scale(outer_surf, (int(outer_surf.get_width() * shrink),
                                                            int(outer_surf.get_height() * shrink)))

    surf = expand_fill_maintaining_ratio(surf, shrunk_outer_surf, ratio)

    # -- center smaller surface --
    surf_pos = (int(outer_surf.get_width() * alignment[0]), int(outer_surf.get_height() * alignment[1]))
    surf_rect = surf.get_rect()
    surf_rect.centerx, surf_rect.centery = surf_pos

    return surf, surf_rect


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
