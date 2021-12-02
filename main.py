import pygame
from window_sizing import ScaleSurface, TextSurface
from tiles import Tile

def game_loop(screen):
    pygame.display.set_caption("Epic chess engine")
    clock = pygame.time.Clock()

    # -- initialise surfaces --
    window = ScaleSurface((23, 89, 101), (16, 9), (0.5, 0.5), 1)

    # - chess board and border -
    chess_board_border = ScaleSurface((0, 0, 0), (1, 1), (0.35, 0.5), 0.9)
    chess_board = ScaleSurface((231, 167, 106), (1, 1), (0.5, 0.5), 0.95)

    # - evaluation bar -
    eval_bar = ScaleSurface((0, 0, 0), (1, 14), (0.045, 0.5), 0.95)
    eval_maximiser = ScaleSurface((231, 118, 106), (1, 15), (0.5, 0.25), 0.8)
    eval_minimiser = ScaleSurface((80, 175, 101), (1, 15), (0.5, 0.75), 0.8)

    # - options menu -
    options_border = ScaleSurface((0, 0, 0), (4, 6), (0.8, 0.5), 0.9)
    # text output
    text_output = TextSurface((255, 0, 0), (5, 3), (0.5, 0.2), 0.9, (255, 255, 255), "win/ lose", 0.4)
    # move hints
    move_hint_label = TextSurface((255, 0, 0), (4, 1), (0.5, 0.5), 0.9, (255, 255, 255), "move hints    ", 0.5)
    move_hint_checkbox = TextSurface((0, 10, 0), (1, 1), (0.9, 0.5), 0.7, (255, 255, 255), "√", 0.45)
    # show engine
    show_engine_label = TextSurface((255, 0, 0), (4, 1), (0.5, 0.7), 0.9, (255, 255, 255), "show engine    ", 0.45)
    show_engine_checkbox = TextSurface((0, 20, 0), (1, 1), (0.9, 0.5), 0.7, (255, 255, 255), "x", 0.45)

    # TODO: tile surfs
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
                text_output.resize(options_border.image)

                move_hint_label.resize(options_border.image)
                move_hint_checkbox.resize(move_hint_label.image)
                show_engine_label.resize(options_border.image)
                show_engine_checkbox.resize(show_engine_label.image)

        # -- blit surfaces --

        # move hints
        move_hint_label.image.blit(move_hint_checkbox.image, move_hint_checkbox.rect)
        options_border.image.blit(move_hint_label.image, move_hint_label.rect)
        # show engine
        show_engine_label.image.blit(show_engine_checkbox.image, show_engine_checkbox.rect)
        options_border.image.blit(show_engine_label.image, show_engine_label.rect)
        # text output
        options_border.image.blit(text_output.image, text_output.rect)
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
