import pygame
from window_sizing import resize_text, ScaleWindow
from tiles import Tile

def game_loop(screen):
    pygame.display.set_caption("Epic chess engine")
    clock = pygame.time.Clock()

    # -- initialise surfaces --
    window = ScaleWindow((23, 89, 101), (16, 9), (0.5, 0.5), 1)

    # - chess board and border -
    chess_board_border = ScaleWindow((0, 0, 0), (1, 1), (0.35, 0.5), 0.95)
    chess_board = ScaleWindow((231, 167, 106), (1, 1), (0.5, 0.5), 0.9)

    # - evaluation bar -
    eval_bar = ScaleWindow((0, 0, 0), (1, 14), (0.045, 0.5), 0.95)
    eval_maximiser = ScaleWindow((231, 118, 106), (1, 15), (0.5, 0.25), 0.8)
    eval_minimiser = ScaleWindow((80, 175, 101), (1, 15), (0.5, 0.75), 0.8)

    # - options menu -
    options_border = ScaleWindow((0, 0, 0), (4, 6), (0.8, 0.5), 0.9)

    # TODO: text output window, tile surfs
    # text_output, text_output_pos = resize_text(0.9, text_output, options_border, (5, 3), (0.5, 0.2))]
    # tile_group.update(chess_board)
    # # tile creation
    # tile_group = pygame.sprite.Group()
    # tile_group.add(Tile(1))

    # -- post resize events --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # second post allows for rendering of text on the now non-zero sized surfaces
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))

    # -- game loop --
    while True:

        screen.fill((6, 65, 76))

        # -- event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -- resize event --
            if event.type == pygame.VIDEORESIZE:

                # -- resize surfaces --
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window.resize(screen)

                chess_board_border.resize(window.image)
                chess_board.resize(chess_board_border.image)

                eval_bar.resize(window.image)
                eval_maximiser.resize(eval_bar.image)
                eval_minimiser.resize(eval_bar.image)

                options_border.resize(window.image)


        # -- blit surfaces --
        window.image.blit(options_border.image, options_border.rect)

        eval_bar.image.blit(eval_maximiser.image, eval_maximiser.rect)
        eval_bar.image.blit(eval_minimiser.image, eval_minimiser.rect)
        window.image.blit(eval_bar.image, eval_bar.rect)

        chess_board_border.image.blit(chess_board.image, chess_board.rect)
        window.image.blit(chess_board_border.image, chess_board_border.rect)

        screen.blit(window.image, window.rect)
        pygame.display.update()

        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    game_loop(pygame.display.set_mode((1, 1), pygame.RESIZABLE))
    pygame.quit()
