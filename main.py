import pygame
from window_sizing import *


def run_engine_window(screen):

    # -- initialise objects --

    pygame.display.set_caption("Epic chess engine")
    clock = pygame.time.Clock()

    window = pygame.Surface((1, 1))

    # -- game loop --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    while True:

        # -- color surfaces --
        screen.fill((0, 0, 255))
        window.fill((102,255,102))

        # -- event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -- resize event --
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                # resize window
                window, window_pos = resize_surface(0.95, window, screen, (1, 1))

        # -- blit surfaces --
        screen.blit(window, (window_pos))
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    main_screen = pygame.display.set_mode((1, 1), pygame.RESIZABLE)
    run_engine_window(main_screen)
    pygame.quit()