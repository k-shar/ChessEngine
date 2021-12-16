# -- imports --
import pygame
import engine_config
from window_sizing import ScaleSurface, TextSurface, ColorThemeButton, HintsToggle, ResetButton
from tiles import Tile
import colors
import random
from bouncing_ball import Bouncy


def game(screen):
    pygame.display.set_caption("Iteration 1.3 chess engine")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    show_ui = True
    balls = []
    SHOW_COORDINATES = False

    """ Initialise Surfaces """

    window = ScaleSurface("WINDOW", (16, 9), (0.5, 0.5), 1)

    # -- chess board and border --
    chess_board_border = ScaleSurface("BORDER", (1, 1), (0.35, 0.5), 0.9)
    chess_board = ScaleSurface("CHESS_BOARD", (1, 1), (0.5, 0.5), 0.95)

    # -- evaluation bar --
    eval_bar_border = ScaleSurface("BORDER", (1, 14), (0.045, 0.5), 0.95)
    eval_maximiser = ScaleSurface("MAXIMISER", (1, 15), (0.5, 0.25), 0.8)
    eval_minimiser = ScaleSurface("MINIMISER", (1, 15), (0.5, 0.75), 0.8)

    # -- options menu --
    options_border = ScaleSurface("BORDER", (4, 6), (0.8, 0.5), 0.9)
    text_output = TextSurface("TEXT_OUTPUT", (7, 2), (0.5, 0.13), 0.93, "win/ lose", 0.4, "TEXT", (1, 1))

    coordinates = HintsToggle((0.5, 0.3), "coordinates   ")
    hint_move = HintsToggle((0.5, 0.44), "move hints   ")
    hint_engine = HintsToggle((0.5, 0.58), "show engine   ")
    reset_board = ResetButton("BORDER", (7, 1), (0.5, 0.92), 0.93, "~ reset board ~", 0.6)

    # -- color theme selection --
    color_theme_label = TextSurface("TEXT_OUTPUT", (7, 1), (0.5, 0.71), 0.93, "Color Themes", 0.6, "TEXT", (1, 1))
    blue = ColorThemeButton((0.15, 0.81), "blue", engine_config.blue_theme)
    purple = ColorThemeButton((0.381, 0.81), "purple", engine_config.purple_theme)
    rainbow = ColorThemeButton((0.61, 0.81), "multi", engine_config.multi_theme)
    random_theme = ColorThemeButton((0.85, 0.81), "random", engine_config.random_theme)

    # -- initialise mouse pointer --
    mouse_pointer_size = 1  # actual size set on resize event
    mouse_pointer = pygame.Surface([mouse_pointer_size] * 2)
    mouse_pointer.set_colorkey((0, 0, 0))
    # - offsets for mouse pointer -
    window_offset = [0, 0]  # distance from window from screen
    options_offset = [0, 0]  # distance from options menu to screen

    """ Tile generation """
    tile_group = []
    white = False
    for col_index in range(1, 9):
        # the color of the first tile of each row alternates
        white = not white
        for row_index in range(1, 9):
            tile_group.append(Tile(col_index, row_index, white))
            white = not white  # tile colors alternate

    # -- surface groups --
    scale_surfs = [window, chess_board, chess_board_border, options_border, reset_board]
    hint_toggles = [hint_move, hint_engine, coordinates]
    static_surfs = [text_output, color_theme_label, eval_bar_border, eval_minimiser, eval_maximiser]
    color_theme_buttons = [blue, purple, rainbow, random_theme]
    all_surfaces = scale_surfs + hint_toggles + static_surfs + color_theme_buttons + tile_group

    """ Color creation """
    # set default color theme
    active_color_theme = blue.click(True)

    # -- generate array of rainbow colors --
    frame = 0
    N = 300
    color_spectrum = colors.rainbow_spectrum(N)
    color_spectrum = color_spectrum * 2  # *2 to avoid an out of phase surface indexing an item out of the array

    # -- initialise fade variables --
    fade_duration = 30
    initial_fade_scale = 1  # how many times longer the opening first fade takes, compared to normal fades
    fade_spectrum_3d = []
    for surf in all_surfaces:
        fade_spectrum_3d.append(
            colors.generate_spectrum(fade_duration * initial_fade_scale, engine_config.multi_theme[surf.name],
                                     engine_config.default_theme[surf.name]))
    fade_counter = fade_duration * initial_fade_scale - 1

    # -- post resize events --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # second post allows for rendering of text on the now non-zero sized surfaces
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))

    """ Game Loop """
    while True:
        """ Update every frame """
        screen.fill(active_color_theme["SCREEN"])

        # -- update frame counter --
        frame += 1
        if frame >= N - 1:
            frame = 0

        # -- rainbow mode --
        if rainbow.clicked:
            chess_board_border.image.fill(color_spectrum[frame + N // 3])
            options_border.image.fill(color_spectrum[frame])
            screen.fill(color_spectrum[frame + N // 4])
            window.image.fill(color_spectrum[frame + N // 2])

        # -- fade between colors --
        if fade_counter > 0:
            for i in range(len(all_surfaces)):
                surf = all_surfaces[i]
                surf.setcolor(fade_spectrum_3d[i][fade_counter])

                if type(surf) == HintsToggle:
                    surf.resize(options_border.image)

            fade_counter -= 1
            if fade_counter == 0:
                # reset surfs to new color set
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                     {"w": screen.get_width(), "h": screen.get_height()}))

        """ Event handler """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            """ resize event"""
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window.resize(screen)

                # mouse pointer
                mouse_pointer.fill((0, 0, 0))
                mouse_pointer_size = screen.get_height() // 40
                mouse_pointer = pygame.transform.scale(mouse_pointer, [mouse_pointer_size] * 2)

                # chess board
                chess_board_border.resize(window.image)
                chess_board.resize(chess_board_border.image)

                for tile in tile_group:
                    tile.resize(chess_board.image)

                # evaluation bar
                eval_bar_border.resize(window.image)
                eval_maximiser.resize(eval_bar_border.image)
                eval_minimiser.resize(eval_bar_border.image)

                # - options menu -
                options_border.resize(window.image)
                text_output.resize(options_border.image)

                # hint buttons
                for surf in hint_toggles:
                    surf.resize(options_border.image)
                reset_board.resize(options_border.image)

                # - color themes -
                color_theme_label.resize(options_border.image)
                for surf in color_theme_buttons:
                    surf.resize(options_border.image)

                # resize button
                reset_board.resize(options_border.image)

                # -- set mouse pointer offsets --
                window_offset = window.rect.topleft
                options_offset = options_border.rect.topleft

            """ any mouse click """
            if event.type == pygame.MOUSEBUTTONUP and not show_ui:
                # -- create bouncer --
                for i in range(30):
                    balls.append(Bouncy(screen.get_size(), (pygame.mouse.get_pos())))

            """ button hover or click """
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and fade_counter <= 0:
                # -- set mouse_pointer offsets and rect --
                relative_to_options = [pygame.mouse.get_pos()[0] - window_offset[0] - options_offset[0],
                                       pygame.mouse.get_pos()[1] - window_offset[1] - options_offset[1]]
                mouse_pointer_rect = pygame.Rect(relative_to_options[0], relative_to_options[1], mouse_pointer_size,
                                                 mouse_pointer_size)

                # reset board option hover
                if reset_board.rect.colliderect(mouse_pointer_rect):
                    reset_board.hover(True)
                    if event.type == pygame.MOUSEBUTTONUP:
                        reset_board.click(True)
                else:
                    reset_board.hover(False)

                # hover for hint toggles
                for hint_button in hint_toggles:
                    if hint_button.rect.colliderect(mouse_pointer_rect):
                        hint_button.hover(True)
                        if event.type == pygame.MOUSEBUTTONUP:
                            hint_button.click(not hint_button.is_clicked)
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                                 {"w": screen.get_width(),
                                                                  "h": screen.get_height()}))

                            # take action depending on what button was pressed
                            if hint_button.active_text == "coordinates   ":
                                SHOW_COORDINATES = not SHOW_COORDINATES
                    else:
                        hint_button.hover(False)

                # check if mouse is hovering over a color theme button
                for theme_button in color_theme_buttons:

                    # -- apply hover effect --
                    if theme_button.rect.colliderect(mouse_pointer_rect):
                        theme_button.hover(True)

                        # -- if mouse is also clicking --
                        if event.type == pygame.MOUSEBUTTONUP:

                            previous_col = active_color_theme
                            # de-select all other buttons
                            for other_button in color_theme_buttons:
                                other_button.click(False)
                            # select clicked button
                            active_color_theme = theme_button.click(True)  # theme button returns its theme dictionary

                            # ensure button was not already selected/ does not recolor in this way
                            if (
                                    previous_col == active_color_theme and active_color_theme != engine_config.random_theme) or \
                                    active_color_theme == engine_config.multi_theme:
                                break

                            # -- if random theme --
                            if active_color_theme == engine_config.random_theme:
                                for surf in scale_surfs + color_theme_buttons + hint_toggles + static_surfs + tile_group:
                                    theme_button.click(False)
                                    # -- generate random color theme --
                                    surf.color_set = {surf.name: (random.randint(0, 255), random.randint(0, 255),
                                                                  random.randint(0, 255)),
                                                      "TEXT": (random.randint(0, 255), random.randint(0, 255),
                                                               random.randint(0, 255)),
                                                      "HOVERED": (random.randint(0, 255), random.randint(0, 255),
                                                                  random.randint(0, 255)),
                                                      "RESET": (random.randint(0, 255), random.randint(0, 255),
                                                                random.randint(0, 255)),
                                                      "WHITE": (random.randint(0, 255), random.randint(0, 255),
                                                                random.randint(0, 255)),
                                                      "BLACK": (random.randint(0, 255), random.randint(0, 255),
                                                                random.randint(0, 255))
                                                      }

                                # post resize event, to re-color surfaces
                                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                                     {"w": screen.get_width(),
                                                                      "h": screen.get_height()}))

                            # -- else apply pre-defined theme --
                            else:
                                for surf in scale_surfs + color_theme_buttons + hint_toggles + static_surfs + tile_group:
                                    surf.color_set = active_color_theme

                                # -- create color fade spectrum --
                                fade_spectrum_3d = []
                                for surf in all_surfaces:
                                    fade_spectrum_3d.append(
                                        colors.generate_spectrum(fade_duration, previous_col[surf.name],
                                                                 active_color_theme[surf.name]))
                                fade_counter = fade_duration - 1

                    else:
                        theme_button.hover(False)


            """ keypress """
            if event.type == pygame.KEYDOWN:
                if event.unicode == "v":
                    show_ui = not show_ui
                if event.unicode == "b":
                    # -- create bouncer --
                    for i in range(500):
                        balls.append(Bouncy(screen.get_size(), (screen.get_width() // 2, screen.get_height() // 2)))

                if event.unicode == "r":
                    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': screen.get_width(),
                                                                             'h': screen.get_height()}))
        """ draw surfaces """
        # draw mouse cursor
        if engine_config.RAINBOW_MOUSE:
            mouse_color = color_spectrum[frame]
        else:
            window.image.fill(window.color)
            mouse_color = (255, 0, 0)

        pygame.draw.circle(mouse_pointer, mouse_color,
                           (mouse_pointer_size // 2, mouse_pointer_size // 2), mouse_pointer_size // 2)

        if len(balls) > 0:
            # draw ball
            for ball in balls:
                pygame.draw.circle(ball.image, color_spectrum[frame],
                                   (mouse_pointer_size // 2, mouse_pointer_size // 2), mouse_pointer_size // 2)
                ball.update(window.image.get_size())

                window.image.blit(ball.image, ball.rect)
            balls.remove(balls[0])

        if show_ui:

            # color themes
            options_border.image.blit(color_theme_label.image, color_theme_label.rect)
            for surf in color_theme_buttons:
                options_border.image.blit(surf.image, surf.rect)

            # hint buttons
            for surf in hint_toggles:
                options_border.image.blit(surf.image, surf.rect)
            options_border.image.blit(reset_board.image, reset_board.rect)

            # text output
            text_output.draw_text(str(len(balls)))
            options_border.image.blit(text_output.image, text_output.rect)
            window.image.blit(options_border.image, options_border.rect)

            # evaluation bar
            eval_bar_border.image.blit(eval_maximiser.image, eval_maximiser.rect)
            eval_bar_border.image.blit(eval_minimiser.image, eval_minimiser.rect)
            window.image.blit(eval_bar_border.image, eval_bar_border.rect)

            # tiles
            for tile in tile_group:
                if SHOW_COORDINATES:
                    tile.active_text = tile.coordinate
                else:
                    tile.active_text = " "

                chess_board.image.blit(tile.image, tile.rect)

            # chess board
            chess_board_border.image.blit(chess_board.image, chess_board.rect)
            window.image.blit(chess_board_border.image, chess_board_border.rect)

            # mouse pointer
            window.image.blit(mouse_pointer, [pygame.mouse.get_pos()[0] - window_offset[0],
                                              pygame.mouse.get_pos()[1] - window_offset[1]])

        # window
        screen.blit(window.image, window.rect)
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    game(pygame.display.set_mode((1, 1), pygame.RESIZABLE))
    pygame.quit()
