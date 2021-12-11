import pygame
from window_sizing import ScaleSurface, TextSurface, Button, ColorThemeButton, HintsToggle, ResetButton
from tiles import Tile
import colors
import random


def game_loop(screen):
    pygame.display.set_caption("Second iteration chess engine")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    col = colors.blue_theme

    # -- initialise surfaces --
    window = ScaleSurface("WINDOW", (16, 9), (0.5, 0.5), 1)

    # - chess board and border -
    chess_board_border = ScaleSurface("BORDER", (1, 1), (0.35, 0.5), 0.9)
    chess_board = ScaleSurface("CHESS_BOARD", (1, 1), (0.5, 0.5), 0.95)

    # - evaluation bar -
    eval_bar_border = ScaleSurface("BORDER", (1, 14), (0.045, 0.5), 0.95)
    eval_maximiser = ScaleSurface("MAXIMISER", (1, 15), (0.5, 0.25), 0.8)
    eval_minimiser = ScaleSurface("MINIMISER", (1, 15), (0.5, 0.75), 0.8)

    # - options menu -
    options_border = ScaleSurface("BORDER", (4, 6), (0.8, 0.5), 0.9)
    # text output
    text_output = TextSurface("TEXT_OUTPUT", (5, 2), (0.5, 0.15), 0.93, "win/ lose", 0.4)

    # move hints
    hint_move = HintsToggle((0.5, 0.37), "move hints   ")
    # show engine
    hint_engine = HintsToggle((0.5, 0.52), "show engine   ")

    # reset board
    reset_board = ResetButton("BORDER", (21, 4), (0.5, 0.92), 0.9, "reset board", 0.6)
    # color schemes
    color_theme_label = TextSurface("TEXT_OUTPUT", (6, 1), (0.5, 0.66), 0.93, "Color Themes", 0.6)

    # - color theme buttons -
    blue = ColorThemeButton((0.15, 0.79), "blue", colors.blue_theme)
    green = ColorThemeButton((0.38, 0.79), "purple", colors.purple_theme)
    rainbow = ColorThemeButton((0.62, 0.79), "multi", colors.multi_theme)
    random_theme = ColorThemeButton((0.85, 0.79), "random", colors.random_theme)

    # set blue theme as default
    blue.click(True)

    # -- mouse pointer dummy values --
    mouse_pointer_size = 1
    mouse_pointer = pygame.Surface([mouse_pointer_size] * 2)
    mouse_pointer.set_colorkey((0, 0, 0))

    # -- mouse pointer offsets --
    window_offset = [0, 0]  # distance from window from screen
    options_offset = [0, 0]  # distance from options menu to screen

    # -- surface groups --
    scale_surfs = [window, chess_board, chess_board_border, options_border]
    other_buttons = [hint_move, hint_engine, reset_board]
    static_surfs = [text_output, color_theme_label, eval_bar_border, eval_minimiser, eval_maximiser]
    color_theme_buttons = [blue, green, rainbow, random_theme]
    all_surfaces = scale_surfs + other_buttons + static_surfs + color_theme_buttons

    # -- post resize events --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # second post allows for rendering of text on the now non-zero sized surfaces
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))

    # -- generate array of rainbow colors --
    frame = 0
    N = 300
    color_spectrum = colors.rainbow_spectrum(N)
    color_spectrum = color_spectrum * 2  # *2 to avoid an out of phase surface indexing an item out of the array

    # -- initialise fade variables --
    fade_duration = 30
    fade_spectrum_3d = []
    for surf in all_surfaces:
        fade_spectrum_3d.append(colors.generate_spectrum(fade_duration*5, colors.multi_theme[surf.name],
                                                         colors.default_theme[surf.name]))
    fade_counter = fade_duration*5 - 1

    # -- game loop --
    while True:

        # -- color surfaces every frame --
        screen.fill(col["SCREEN"])

        # draw mouse cursor
        pygame.draw.circle(mouse_pointer, color_spectrum[frame],
                           (mouse_pointer_size // 2, mouse_pointer_size // 2), mouse_pointer_size // 2)
        # -- rainbow mode --
        if rainbow.clicked:
            chess_board_border.image.fill(color_spectrum[frame + N // 3])
            options_border.image.fill(color_spectrum[frame])
            screen.fill(color_spectrum[frame + N // 4])
            window.image.fill(color_spectrum[frame + N // 2])

        # -- update frame counter --
        frame += 1
        if frame >= N - 1:
            frame = 0

        # -- fade between colors --
        if fade_counter > 0:
            for i in range(len(all_surfaces)):
                surf = all_surfaces[i]
                surf.setcolor(fade_spectrum_3d[i][fade_counter])

                if type(surf) == HintsToggle:
                    surf.resize(options_border.image)

            fade_counter -= 1
            # reset surfs to original (new) color set
            if fade_counter == 0:
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                     {"w": screen.get_width(), "h": screen.get_height()}))

        # -- event handler --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -- resize event --
            if event.type == pygame.VIDEORESIZE:
                # -- resize surfaces --
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window.resize(screen)

                # mouse pointer
                mouse_pointer.fill((0, 0, 0))
                mouse_pointer_size = screen.get_height() // 40
                mouse_pointer = pygame.transform.scale(mouse_pointer, [mouse_pointer_size] * 2)

                # chess board
                chess_board_border.resize(window.image)
                chess_board.resize(chess_board_border.image)

                # evaluation bar
                eval_bar_border.resize(window.image)
                eval_maximiser.resize(eval_bar_border.image)
                eval_minimiser.resize(eval_bar_border.image)

                # - options menu -
                options_border.resize(window.image)
                text_output.resize(options_border.image)

                # hint buttons
                hint_move.resize(options_border.image)
                hint_engine.resize(options_border.image)

                # - color themes -
                color_theme_label.resize(options_border.image)
                blue.resize(options_border.image)
                green.resize(options_border.image)
                random_theme.resize(options_border.image)
                rainbow.resize(options_border.image)

                # resize button
                reset_board.resize(options_border.image)

                # -- set mouse pointer offsets --
                window_offset = window.rect.topleft
                options_offset = options_border.rect.topleft

            # -- button hover and click --
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and fade_counter <= 0:
                # -- set mouse_pointer offsets and rect --
                relative_to_options = [pygame.mouse.get_pos()[0] - window_offset[0] - options_offset[0],
                                       pygame.mouse.get_pos()[1] - window_offset[1] - options_offset[1]]
                mouse_pointer_rect = pygame.Rect(relative_to_options[0], relative_to_options[1], mouse_pointer_size,
                                                 mouse_pointer_size)

                # check if mouse is hovering over a color theme button
                for theme_button in color_theme_buttons:

                    # -- apply hover effect --
                    if theme_button.rect.colliderect(mouse_pointer_rect):
                        theme_button.hover(True)

                        # -- on mouse click --
                        if event.type == pygame.MOUSEBUTTONUP:
                            # store previous color theme
                            previous_col = col
                            # de-select all other buttons
                            for other_button in color_theme_buttons:
                                other_button.click(False)
                            # select clicked button
                            col = theme_button.click(True)  # theme button returns its theme dictionary

                            # ensue button was not already selected
                            if (previous_col == col and col != colors.random_theme) or col == colors.multi_theme:
                                break

                            # -- if random theme --
                            if col == colors.random_theme:
                                for surf in scale_surfs + color_theme_buttons + other_buttons + static_surfs:
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
                                                      }

                                    # post resize event, to re-color surfaces
                                    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                                         {"w": screen.get_width(),
                                                                          "h": screen.get_height()}))

                            # -- else apply pre-defined theme --
                            else:
                                for surf in scale_surfs + color_theme_buttons + other_buttons + static_surfs:
                                    surf.color_set = col

                                # -- create color fade spectrum --
                                fade_spectrum_3d = []
                                for surf in all_surfaces:
                                    fade_spectrum_3d.append(
                                        colors.generate_spectrum(fade_duration, previous_col[surf.name], col[surf.name]))
                                fade_counter = fade_duration - 1

                    else:
                        theme_button.hover(False)

                # TODO: make more specific
                for button in other_buttons:
                    if button.rect.colliderect(mouse_pointer_rect):
                        button.hover(True)
                    else:
                        button.hover(False)

        # -- blit surfaces --

        # reset board
        options_border.image.blit(reset_board.image, reset_board.rect)

        # color themes
        options_border.image.blit(blue.image, blue.rect)
        options_border.image.blit(green.image, green.rect)
        options_border.image.blit(rainbow.image, rainbow.rect)
        options_border.image.blit(random_theme.image, random_theme.rect)
        options_border.image.blit(color_theme_label.image, color_theme_label.rect)

        # hint buttons
        options_border.image.blit(hint_move.image, hint_move.rect)
        options_border.image.blit(hint_engine.image, hint_engine.rect)

        # text output
        options_border.image.blit(text_output.image, text_output.rect)
        window.image.blit(options_border.image, options_border.rect)

        # evaluation bar
        eval_bar_border.image.blit(eval_maximiser.image, eval_maximiser.rect)
        eval_bar_border.image.blit(eval_minimiser.image, eval_minimiser.rect)
        window.image.blit(eval_bar_border.image, eval_bar_border.rect)

        # chess board
        chess_board_border.image.blit(chess_board.image, chess_board.rect)
        window.image.blit(chess_board_border.image, chess_board_border.rect)

        window.image.blit(mouse_pointer, [pygame.mouse.get_pos()[0] - window_offset[0],
                                          pygame.mouse.get_pos()[1] - window_offset[1]])
        screen.blit(window.image, window.rect)
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    game_loop(pygame.display.set_mode((1, 1), pygame.RESIZABLE))
    pygame.quit()
