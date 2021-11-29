import pygame


def expand_to_fill_with_ratio(smaller, larger, ratio):
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


def resize_surface(shrink, surf, outer_surf, ratio):
    if type(shrink) != float or not(0 < shrink <= 1):
        raise ValueError("shrink must be float between 0 and 1")

    # -- create padding between outer and inner --
    # create a shrunk outer surface to use instead, so when the inner surface is expanded there will be some gap
    # "shrink": float from 0-1 determining how much of the outer surface the inner will fill
    shrunk_outer_surf = pygame.transform.scale(outer_surf, (int(outer_surf.get_width() * shrink),
                                                            int(outer_surf.get_height() * shrink)))

    surf = expand_to_fill_with_ratio(surf, shrunk_outer_surf, ratio)



    # -- center smaller surface --
    surf_pos = (int(outer_surf.get_width() * 0.5), int(outer_surf.get_height() * 0.5))
    surf_rect = surf.get_rect()
    surf_rect.centerx, surf_rect.centery = surf_pos

    return surf, surf_rect