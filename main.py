import pygame
from window_sizing import ScaleSurface, TextSurface, Button
from tiles import Tile
from colors import generate_color_spectrum


def game_loop(screen):

    pygame.display.set_caption("Second iteration chess engine")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # -- initialise surfaces --
    window = ScaleSurface((23, 89, 101), (16, 9), (0.5, 0.5), 1)

    # - chess board and border -
    chess_board_border = ScaleSurface((0, 0, 0), (1, 1), (0.35, 0.5), 0.9)
    chess_board = ScaleSurface((190, 183, 223), (1, 1), (0.5, 0.5), 0.95)

    # - evaluation bar -
    eval_bar = ScaleSurface((0, 0, 0), (1, 14), (0.045, 0.5), 0.95)
    eval_maximiser = ScaleSurface((231, 118, 106), (1, 15), (0.5, 0.25), 0.8)
    eval_minimiser = ScaleSurface((80, 175, 101), (1, 15), (0.5, 0.75), 0.8)

    # - options menu -
    options_border = ScaleSurface((0, 0, 0), (4, 6), (0.8, 0.5), 0.9)
    # text output
    text_output = TextSurface((80, 175, 223), (5, 2), (0.5, 0.15), 0.9, (255, 255, 255), "win/ lose", 0.4)
    # move hints
    move_hint_label = Button((162, 163, 187), (4, 1), (0.5, 0.37), 0.9, (255, 255, 255), "move hints   ", 0.5, (255, 100, 100))
    move_hint_checkbox = TextSurface((0, 5, 3), (1, 1), (0.9, 0.5), 0.7, (255, 255, 255), "√", 0.9)
    # show engine
    show_engine_label = Button((162, 163, 187), (4, 1), (0.5, 0.52), 0.9, (255, 255, 255), "show engine   ", 0.5, (255, 100, 100))
    show_engine_checkbox = TextSurface((0, 20, 0), (1, 1), (0.9, 0.5), 0.7, (255, 255, 255), "x", 0.9)
    # reset board
    reset_board = Button((255, 0, 0), (4, 1), (0.5, 0.9), 0.9, (255, 255, 255), "reset board", 0.6, (0, 0, 0))
    # color schemes
    color_theme_border = TextSurface((70, 0, 200), (6, 1), (0.5, 0.66), 0.9, (255, 255, 255), "Color Themes", 0.6)
    red = Button((255, 0, 0), (4, 3), (0.25, 0.75), 0.2, (255, 255, 255), "x", 0.9, (100, 100, 255))
    green = Button((0, 255, 0), (4, 3), (0.5, 0.75), 0.2, (255, 255, 255), "√", 0.9, (100, 100, 255))
    blue = Button((0, 0, 255), (4, 3), (0.75, 0.75), 0.2, (255, 255, 255), "x", 0.9, (100, 100, 255))

    # -- mouse pointer --
    mouse_pointer = pygame.Surface((10, 10))
    mouse_pointer.fill((0, 255, 255))

    window_offset = [0, 0]  # distance from window from screen
    options_offset = [0, 0]  # distance from options menu to screen

    # -- add buttons to group --
    buttons = [red, green, blue, move_hint_label, move_hint_checkbox, show_engine_checkbox, show_engine_label, reset_board]

    # TODO: tile surfs
    # tile_group.update(chess_board)
    # # tile creation
    # tile_group = pygame.sprite.Group()
    # tile_group.add(Tile(1))

    # -- post resize events --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # second post allows for rendering of text on the now non-zero sized surfaces
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))

    # -- generate rainbow colors --
    frame = 0
    N = 1000
    color_spectrum = generate_color_spectrum(N)

    # -- game loop --
    while True:

        # -- color surfaces every frame --
        screen.fill((6, 65, 76))
        chess_board_border.image.fill((color_spectrum[frame]))
        options_border.image.fill((color_spectrum[frame]))

        # -- update frame counter --
        frame += 1
        if frame >= N-1:
            frame = 0

        # -- event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -- resize event --
            if event.type == pygame.VIDEORESIZE:

                # -- resize surfaces --
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window.resize(screen)

                # chess board
                chess_board_border.resize(window.image)
                chess_board.resize(chess_board_border.image)

                # evaluation bar
                eval_bar.resize(window.image)
                eval_maximiser.resize(eval_bar.image)
                eval_minimiser.resize(eval_bar.image)

                # - options menu -
                options_border.resize(window.image)
                text_output.resize(options_border.image)

                # move hint button
                move_hint_label.resize(options_border.image)
                move_hint_checkbox.resize(move_hint_label.image)

                # show engine button
                show_engine_label.resize(options_border.image)
                show_engine_checkbox.resize(show_engine_label.image)

                # - color themes -
                color_theme_border.resize(options_border.image)
                red.resize(options_border.image)
                green.resize(options_border.image)
                blue.resize(options_border.image)

                # resize button
                reset_board.resize(options_border.image)

                # -- set mouse pointer offsets --
                window_offset = window.rect.topleft
                options_offset = options_border.rect.topleft

            # -- mouse move --
            if event.type == pygame.MOUSEMOTION:
                # -- set mouse_pointer offsets --
                relative_to_options = [pygame.mouse.get_pos()[0] - window_offset[0] - options_offset[0],
                                       pygame.mouse.get_pos()[1] - window_offset[1] - options_offset[1]]

                # check if mouse is hovering over a button
                for button in buttons:
                    if button.rect.collidepoint(relative_to_options):
                        button.update(True)
                    else:
                        button.update(False)

        # -- blit surfaces --

        # reset board
        options_border.image.blit(reset_board.image, reset_board.rect)

        # color themes
        options_border.image.blit(red.image, red.rect)
        options_border.image.blit(blue.image, blue.rect)
        options_border.image.blit(green.image, green.rect)
        options_border.image.blit(color_theme_border.image, color_theme_border.rect)

        # move hints
        move_hint_label.image.blit(move_hint_checkbox.image, move_hint_checkbox.rect)
        options_border.image.blit(move_hint_label.image, move_hint_label.rect)

        # show engine
        show_engine_label.image.blit(show_engine_checkbox.image, show_engine_checkbox.rect)
        options_border.image.blit(show_engine_label.image, show_engine_label.rect)

        # text output
        options_border.image.blit(text_output.image, text_output.rect)
        window.image.blit(options_border.image, options_border.rect)

        # evaluation bar
        eval_bar.image.blit(eval_maximiser.image, eval_maximiser.rect)
        eval_bar.image.blit(eval_minimiser.image, eval_minimiser.rect)
        window.image.blit(eval_bar.image, eval_bar.rect)

        # chess board
        chess_board_border.image.blit(chess_board.image, chess_board.rect)
        window.image.blit(chess_board_border.image, chess_board_border.rect)

        window.image.blit(mouse_pointer, [pygame.mouse.get_pos()[0] - window_offset[0],
                                          pygame.mouse.get_pos()[1] - window_offset[1]])
        screen.blit(window.image, window.rect)
        pygame.display.update()

        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    game_loop(pygame.display.set_mode((1, 1), pygame.RESIZABLE))
    pygame.quit()
