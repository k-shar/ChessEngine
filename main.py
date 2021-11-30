import pygame
from window_sizing import resize_surface

def game_loop(screen):
    pygame.display.set_caption("Epic chess engine")
    clock = pygame.time.Clock()

    # the actual surface dimensions are set in the resize event
    size_placeholder = (1, 1)

    # -- initialise objects --
    window = pygame.Surface(size_placeholder)

    chess_board = pygame.Surface(size_placeholder)
    chess_board_border = pygame.Surface(size_placeholder)

    eval_bar = pygame.Surface(size_placeholder)
    eval_maximiser = pygame.Surface(size_placeholder)  # the chess engine
    eval_minimiser = pygame.Surface(size_placeholder)  # user, displayed beneath the engine

    options_border = pygame.Surface(size_placeholder)

    # post the first resize event
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # -- game loop --
    while True:

        # -- color surfaces --
        screen.fill((6, 65, 76))
        window.fill((23, 89, 101))

        chess_board.fill((231, 167, 106))
        chess_board_border.fill((0, 0, 0))

        eval_bar.fill((0, 0, 0))
        eval_maximiser.fill((231, 118, 106))
        eval_minimiser.fill((80, 175, 101))

        options_border.fill((0, 0, 0))

        # -- event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -- resize event --
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                window, window_pos = resize_surface(1, window, screen, (13, 9), (0.5, 0.5))

                chess_board_border, chess_board_border_pos = resize_surface(0.9, chess_board_border, window, (1, 1), (0.4, 0.5))
                chess_board, chess_board_pos = resize_surface(0.95, chess_board, chess_board_border, (1, 1), (0.5, 0.5))

                eval_bar, eval_bar_pos = resize_surface(1, eval_bar, window, (1, 19), (0.03, 0.5))
                eval_maximiser, eval_maximiser_pos = resize_surface(0.9, eval_maximiser, eval_bar, (1, 15), (0.5, 0.25))
                eval_minimiser, eval_minimiser_pos = resize_surface(0.9, eval_minimiser, eval_bar, (1, 15), (0.5, 0.75))

                options_border, options_border_pos = resize_surface(0.9, options_border, window, (4, 11), (0.85, 0.5))
        # -- blit surfaces --

        chess_board_border.blit(chess_board, (chess_board_pos))
        window.blit(chess_board_border, (chess_board_border_pos))

        eval_bar.blit(eval_maximiser, ((eval_maximiser_pos)))
        eval_bar.blit(eval_minimiser, (eval_minimiser_pos))
        window.blit(eval_bar, (eval_bar_pos))

        window.blit(options_border, (options_border_pos))

        screen.blit(window, (window_pos))
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    main_screen = pygame.display.set_mode((1, 1), pygame.RESIZABLE)
    game_loop(main_screen)
    pygame.quit()
