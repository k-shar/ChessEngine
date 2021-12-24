# -- imports --
import pygame
from engine_config import *
from window_sizing import ScaleSurface, TextSurface, ColorThemeButton, HintsToggle, ResetButton, EvaluationSlider, EvaluationTextSlider
from tiles import Tile
from pieces import *
from fen_manipulation import is_valid_fen, make_move_on_FEN
from evaluation import generate_evaluation_spectrum, normalise_evaluation
import colors
import random
from bouncing_ball import Bouncy


def game(screen):
    pygame.display.set_caption("Iteration 1.7 chess engine")
    clock = pygame.time.Clock()
    # pygame.mouse.set_visible(False)

    active_piece = None
    show_ui = True
    show_coordinates = False
    player_move = None
    balls = []
    legal_tile_indices = []
    fade_indexer = 0
    evaluation = 0.5
    evaluation_transition = [evaluation]

    # STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
    STARTING_FEN = "rnbqkbnr/pppppppp/11111111/1111R111/11111111/11111r11/PPPPPPPP/RNBQKBNR w KQkq"
    STARTING_FEN = "1111p111/111111P1/1B11Qqn1/1N11R11k/1K1b111N/n1111r11/b111B111/11Q111q1 w KQkq"
    STARTING_FEN = "1B11111p/ppppp11b/1111B111/111r111b/11111111/11111111/1PPPPR11/11111P11 w KQkq"
    STARTING_FEN = "rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/PPPPPPPP/RNBQKBNR w KQkq"

    is_valid_fen(STARTING_FEN)
    active_FEN = STARTING_FEN

    """ Initialise Surfaces """
    window = ScaleSurface("WINDOW", (16, 9), (0.5, 0.5), 1)

    fps_counter = TextSurface("BORDER", (5, 3), (0.05, 0.05), 0.08, "0.0", 0.6, "TEXT", (1, 1))

    # -- chess board and border --
    chess_board_border = ScaleSurface("BORDER", (1, 1), (0.35, 0.5), 0.9)
    chess_board = ScaleSurface("BLACK", (1, 1), (0.5, 0.5), 0.95)

    # -- evaluation bar --
    eval_bar_border = ScaleSurface("WINDOW", (1, 10), (0.045, 0.5), 0.95)
    eval_maximiser = EvaluationSlider("BLACK", True)
    eval_minimiser = EvaluationSlider("WHITE", False)
    eval_label_border = EvaluationTextSlider("BORDER", (5, 3), (0.5, 0.5), 1, "0.0", 0.5, "WHITE", (1, 1))
    eval_label = TextSurface("TEXT_OUTPUT", (5, 3), (0.5, 0.5), 0.9, "0.0", 0.5, "BORDER", (1, 1))

    # -- options menu --
    options_border = ScaleSurface("BORDER", (4, 6), (0.8, 0.5), 0.9)
    text_output = TextSurface("TEXT_OUTPUT", (7, 2), (0.5, 0.13), 0.93, "win/ lose", 0.4, "TEXT", (1, 1))

    coordinates = HintsToggle((0.5, 0.3), "coordinates   ")
    hint_move = HintsToggle((0.5, 0.44), "move hints   ")
    hint_engine = HintsToggle((0.5, 0.58), "show engine   ")
    reset_board = ResetButton("BORDER", (7, 1), (0.5, 0.92), 0.93, "~ reset board ~", 0.6)

    # -- color theme selection --
    color_theme_label = TextSurface("TEXT_OUTPUT", (7, 1), (0.5, 0.71), 0.93, "Color Themes", 0.6, "TEXT", (1, 1))
    blue = ColorThemeButton((0.15, 0.81), "blue", blue_theme)
    purple = ColorThemeButton((0.381, 0.81), "purple", purple_theme)
    multi = ColorThemeButton((0.61, 0.81), "multi", all_black)
    green = ColorThemeButton((0.85, 0.81), "green", green_theme)

    # -- initialise mouse pointer --
    mouse_pointer = pygame.Surface([1, 1])
    mouse_pointer.set_colorkey((0, 0, 0))

    """ Tile generation """
    tile_group = []
    white = False
    for row_index in range(1, 9):
        white = not white
        for col_index in range(1, 9):
            tile_group.append(Tile(col_index, row_index, white, len(tile_group)))
            white = not white  # tile colors alternate

    """ Piece generation """
    piece_group = instasiate_pieces(STARTING_FEN)

    # -- surface groups --
    scale_surf_group = [window, chess_board, chess_board_border, options_border, reset_board]
    hint_toggle_group = [hint_move, hint_engine, coordinates]
    static_surf_group = [text_output, color_theme_label, eval_bar_border, eval_minimiser, eval_maximiser, eval_label, eval_label_border]
    color_theme_button_group = [blue, purple, multi, green]
    all_surfaces_group = scale_surf_group + hint_toggle_group + static_surf_group + color_theme_button_group + tile_group

    """ Color creation """
    # set default color theme
    current_color_theme = blue.click(True)

    # -- generate array of rainbow colors --
    frame = 0
    color_spectrum = colors.rainbow_spectrum(RAINBOW_COLOR_SPECTRUM_SIZE) * 2  # * 2 to allow phase differences

    # -- post resize events --
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))
    # second post allows for rendering of text on the now non-zero sized surfaces
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 600, 'h': 400}))

    """ Game Loop """
    while True:

        # -- update frame counter --
        frame += 1
        if frame >= RAINBOW_COLOR_SPECTRUM_SIZE - 1:  # loop frame counter back
            frame = 0

        # -- rainbow spectrum multi color mode --
        if multi.clicked:
            chess_board_border.image.fill(color_spectrum[frame + RAINBOW_COLOR_SPECTRUM_SIZE // 3])
            options_border.image.fill(color_spectrum[frame])
            screen.fill(color_spectrum[frame + RAINBOW_COLOR_SPECTRUM_SIZE // 4])
            window.image.fill(color_spectrum[frame + RAINBOW_COLOR_SPECTRUM_SIZE // 2])
            eval_bar_border.image.fill(color_spectrum[frame + RAINBOW_COLOR_SPECTRUM_SIZE // 2])
            eval_label_border.image.fill(color_spectrum[frame])
            eval_label_border.image.blit(eval_label.image, eval_label.rect)
        else:
            screen.fill(current_color_theme["SCREEN"])

        if not MOUSE_TRAIL and len(balls) == 0 and not multi.clicked:
            window.image.fill(current_color_theme["WINDOW"])

        # -- fade between colors, if in transition --
        if fade_indexer > 0:
            # set screen to follow window color
            screen.fill(fade_spectrum_3d[0][fade_indexer])
            for i in range(len(all_surfaces_group)):
                surf = all_surfaces_group[i]
                surf.setcolor(fade_spectrum_3d[i][fade_indexer])

                # ensure checkbox still dispalys
                if type(surf) == HintsToggle:
                    surf.draw_checkbox()

            fade_indexer -= 1
            if fade_indexer == 0:
                # reset surfs to new color set
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                     {"w": screen.get_width(), "h": screen.get_height()}))

        # -- update evaluation bar --
        if len(evaluation_transition) > 0:
            eval_maximiser.set_slide(evaluation_transition[-1])
            eval_minimiser.set_slide(evaluation_transition[-1])
            eval_label_border.set_slide(evaluation_transition[-1])

            # redraw the new surfs
            eval_bar_border.resize(window.image)
            eval_maximiser.resize(eval_bar_border.image)
            eval_minimiser.resize(eval_bar_border.image)
            eval_label_border.resize(eval_bar_border.image)
            if multi.clicked:
                eval_bar_border.image.fill(color_spectrum[frame + RAINBOW_COLOR_SPECTRUM_SIZE // 2])
                eval_label_border.image.fill(color_spectrum[frame])
            eval_label.draw_text(f"{float(str(evaluation_transition[-1])[:4]):.2f}")
            eval_label_border.image.blit(eval_label.image, eval_label.rect)

            evaluation_transition.pop()

        """ Event handler """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            """ resize event"""
            if event.type == pygame.VIDEORESIZE:

                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window.resize(screen)
                fps_counter.resize(window.image)

                # mouse pointer
                mouse_pointer.fill((0, 0, 0))
                mouse_pointer_size = screen.get_height() // 40
                mouse_pointer = pygame.transform.scale(mouse_pointer, [mouse_pointer_size, mouse_pointer_size])

                # chess board
                chess_board_border.resize(window.image)
                chess_board.resize(chess_board_border.image)

                # tiles
                for tile in tile_group:
                    tile.resize(chess_board.image)

                # pieces
                for piece in piece_group:
                    piece.resize(tile_group[piece.tile_index].image.get_rect().size, 1)

                # evaluation bar
                eval_bar_border.resize(window.image)
                eval_maximiser.resize(eval_bar_border.image)
                eval_minimiser.resize(eval_bar_border.image)
                eval_label_border.resize(eval_bar_border.image)
                eval_label.resize(eval_label_border.image)

                # - options menu -
                options_border.resize(window.image)
                text_output.resize(options_border.image)

                # hint buttons
                for surf in hint_toggle_group:
                    surf.resize(options_border.image)
                reset_board.resize(options_border.image)

                # - color themes -
                color_theme_label.resize(options_border.image)
                for surf in color_theme_button_group:
                    surf.resize(options_border.image)

                # resize button
                reset_board.resize(options_border.image)

                # -- set mouse pointer offsets for collisions --
                window_offset = window.rect.topleft
                options_offset = options_border.rect.topleft
                chess_board_offset = [chess_board.rect.topleft[0] + chess_board_border.rect.topleft[0] + window_offset[0],
                                      chess_board.rect.topleft[1] + chess_board_border.rect.topleft[1] + window_offset[1]]


            """ - hover or click events - """
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and fade_indexer <= 0:
                # -- set mouse_pointer offsets and rect --
                relative_to_options = [pygame.mouse.get_pos()[0] - window_offset[0] - options_offset[0],
                                       pygame.mouse.get_pos()[1] - window_offset[1] - options_offset[1]]

                mouse_pointer_rect = pygame.Rect(relative_to_options[0], relative_to_options[1],
                                                 mouse_pointer_size, mouse_pointer_size)

                """ HOVERING OVER CHESS BOARD """
                if chess_board_border.image.get_rect().collidepoint([pygame.mouse.get_pos()[0] - chess_board_offset[0],
                                                                     pygame.mouse.get_pos()[1] - chess_board_offset[1]]):

                    """ piece highlight on hover """
                    tile_size = tile_group[0].rect.width
                    for piece in piece_group:
                        tile_offset = [tile_group[piece.tile_index].pos[0] * tile_size - tile_size,
                                       tile_group[piece.tile_index].pos[1] * tile_size - tile_size]
                        if piece.image.get_rect().collidepoint([pygame.mouse.get_pos()[0] - chess_board_offset[0] - tile_offset[0],
                                                                pygame.mouse.get_pos()[1] - chess_board_offset[1] - tile_offset[1]]):
                            piece.hover(True)

                            # if mouse is also clicked, select piece
                            if event.type == pygame.MOUSEBUTTONUP and active_piece is None:
                                for other_piece in piece_group:
                                    other_piece.selected = False
                                piece.selected = True

                        else:
                            piece.hover(False)

                    """ tiles hover """
                    # if mouse clicked and hovered
                    if event.type == pygame.MOUSEBUTTONUP and active_piece is not None:
                        legal_tile_indices = active_piece.generate_legal_moves(tile_group, piece_group)

                        # if a piece is selected, place it on this tile
                        for tile_index in legal_tile_indices:
                            tile = tile_group[tile_index]
                            tile_offset = [tile.pos[0] * tile_size - tile_size,
                                           tile.pos[1] * tile_size - tile_size]

                            if tile.image.get_rect().collidepoint([pygame.mouse.get_pos()[0] - chess_board_offset[0] - tile_offset[0],
                                                                   pygame.mouse.get_pos()[1] - chess_board_offset[1] - tile_offset[1]]):

                                old_tile = tile_group[active_piece.tile_index]
                                old_tile.image.fill(old_tile.color)

                                # if tile is occupied
                                occupying_piece = None
                                friendly_piece = False
                                for old_piece in piece_group:
                                    if old_piece.tile_index == tile.tile_index:
                                        occupying_piece = old_piece
                                        if occupying_piece.color == active_piece.color:
                                            friendly_piece = True

                                if not friendly_piece:
                                    if occupying_piece is not None:
                                        # if enemy piece
                                        piece_group.remove(occupying_piece)
                                    # place the piece
                                    active_piece.tile_index = tile.tile_index
                                    # log the piece move
                                    player_move = active_piece.name, tile.coordinate, tile.pos
                                    active_FEN = make_move_on_FEN(active_FEN, player_move, old_tile.pos)

                        # deselect piece
                        active_piece.selected = False
                        active_piece = None

                    # else:
                    #     # not hovered
                    #     tile.draw_text(tile.active_text)


                """ HOVERING OVER OPTIONS BORDER """
                """ hint toggle hover """
                for hint_button in hint_toggle_group:
                    if hint_button.rect.colliderect(mouse_pointer_rect):
                        hint_button.hover(True)

                        """ hint toggle click """
                        if event.type == pygame.MOUSEBUTTONUP:
                            hint_button.click(not hint_button.is_clicked)  # toggle
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,
                                                                 {"w": screen.get_width(),
                                                                  "h": screen.get_height()}))

                            # take action depending on what button was pressed
                            if hint_button.active_text == "coordinates   ":
                                show_coordinates = not show_coordinates
                    else:
                        hint_button.hover(False)

                """ color theme button hover """
                for theme_button in color_theme_button_group:

                    # -- apply hover effect --
                    if theme_button.rect.colliderect(mouse_pointer_rect):
                        theme_button.hover(True)

                        """ color theme click """
                        if event.type == pygame.MOUSEBUTTONUP:

                            previous_col = current_color_theme
                            # de-select all other color theme buttons
                            for other_button in color_theme_button_group:
                                other_button.click(False)
                            # select button just clicked
                            current_color_theme = theme_button.click(True)  # theme button returns its theme dictionary

                            # ensure button was not already selected
                            if previous_col == current_color_theme or multi.clicked:
                                break

                            # update all surfs with new colors
                            for surf in all_surfaces_group:
                                surf.color_set = current_color_theme
                            for tile in tile_group:
                                tile.color_set = current_color_theme
                                tile.setcolor(None)

                            # -- create color fade spectrum --
                            fade_spectrum_3d = []
                            for surf in all_surfaces_group:
                                fade_spectrum_3d.append(
                                    colors.generate_spectrum(FADE_DURATION, previous_col[surf.name],
                                                             current_color_theme[surf.name]))
                            fade_indexer = FADE_DURATION - 1

                    # if there was no collision for the color theme button
                    else:
                        theme_button.hover(False)

                """ reset-board option hover """
                if reset_board.rect.colliderect(mouse_pointer_rect):
                    reset_board.hover(True)
                    if event.type == pygame.MOUSEBUTTONUP:
                        reset_board.click(True)

                        # clear all tiles to remove old piece sprites
                        for tile in tile_group:
                            tile.image.fill(tile.color)

                        piece_group = instasiate_pieces(STARTING_FEN)
                        # size pieces up
                        for piece in piece_group:
                            piece.resize(tile_group[piece.tile_index].image.get_rect().size, 1)
                else:
                    reset_board.hover(False)

            """ keypress """
            if event.type == pygame.KEYDOWN:
                if event.unicode == "v":
                    show_ui = not show_ui
                if event.unicode == "m":
                    multi.click(not multi.clicked)
                    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': screen.get_width(),
                                                                              'h': screen.get_height()}))
                if event.unicode == "b":
                    # -- create bouncer --
                    for i in range(500):
                        balls.append(Bouncy(screen.get_size(), (screen.get_width() // 2, screen.get_height() // 2)))

                if event.unicode == "r":
                    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': screen.get_width(),
                                                                              'h': screen.get_height()}))
                if event.unicode == "t":
                    evaluation = random.randint(-10, 10)
                    if len(evaluation_transition) > 0:
                        evaluation_transition = generate_evaluation_spectrum(evaluation_transition[-1], evaluation)
                    else:
                        evaluation_transition = generate_evaluation_spectrum(eval_minimiser.slide, evaluation)

        """ draw mouse pointer """
        if RAINBOW_MOUSE:
            mouse_color = color_spectrum[frame]
        else:
            if not multi.clicked and len(balls) == 0:
                window.image.fill(window.color)
            mouse_color = (255, 0, 0)
        pygame.draw.circle(mouse_pointer, mouse_color,
                          (mouse_pointer_size // 2, mouse_pointer_size // 2), mouse_pointer_size // 2)

        """ draw balls """
        if len(balls) > 0:
            # draw ball
            for ball in balls:
                pygame.draw.circle(ball.image, color_spectrum[frame],
                                   (mouse_pointer_size // 2, mouse_pointer_size // 2), mouse_pointer_size // 2)
                ball.update(window.image.get_size())

                window.image.blit(ball.image, ball.rect)
            balls.remove(balls[0])

        """ draw ui """
        if show_ui:
            # color themes
            options_border.image.blit(color_theme_label.image, color_theme_label.rect)
            for surf in color_theme_button_group:
                options_border.image.blit(surf.image, surf.rect)

            # hint buttons
            for surf in hint_toggle_group:
                options_border.image.blit(surf.image, surf.rect)
            options_border.image.blit(reset_board.image, reset_board.rect)

            # text output
            text_output.draw_text(str(player_move))
            options_border.image.blit(text_output.image, text_output.rect)
            window.image.blit(options_border.image, options_border.rect)

            # evaluation bar
            eval_bar_border.image.blit(eval_maximiser.image, eval_maximiser.rect)
            eval_bar_border.image.blit(eval_minimiser.image, eval_minimiser.rect)
            eval_bar_border.image.blit(eval_label_border.image, eval_label_border.rect)
            eval_label_border.image.blit(eval_label.image, eval_label.rect)
            window.image.blit(eval_bar_border.image, eval_bar_border.rect)

            if active_piece is not None:
                legal_tile_indices = active_piece.generate_legal_moves(tile_group, piece_group)
                for tile_index in legal_tile_indices:

                    tile_group[tile_index].is_legal_move = True
                    # draw dot on legal move square
                    pygame.draw.ellipse(tile_group[tile_index].image, current_color_theme["LEGAL_MOVE"],
                                        [tile_group[tile_index].image.get_height() // 4,
                                         tile_group[tile_index].image.get_width() // 4,
                                         tile_group[tile_index].image.get_height() // 2,
                                         tile_group[tile_index].image.get_width() // 2])

            # pieces
            for piece in piece_group:
                tile = tile_group[piece.tile_index]
                tile.image.blit(piece.image, piece.rect)
                if tile.is_legal_move:
                    tile.is_legal_move = False
                    pygame.draw.ellipse(tile.image, current_color_theme["CAPTURE_SQUARE"],
                                        tile.image.get_rect())
                    tile.image.blit(piece.image, piece.rect)
                if piece.selected:
                    active_piece = piece
                    tile.image.fill(tile.color_set["HOVERED"])

            # blit tile and coordinates to board
            for tile in tile_group:
                if show_coordinates:
                    tile.active_text = tile.coordinate
                else:
                    tile.active_text = " "
                chess_board.image.blit(tile.image, tile.rect)
                tile.image.fill(tile.color)
                tile.draw_text(tile.active_text)



            # chess board
            chess_board_border.image.blit(chess_board.image, chess_board.rect)
            window.image.blit(chess_board_border.image, chess_board_border.rect)

            # mouse pointer
            window.image.blit(mouse_pointer, [pygame.mouse.get_pos()[0] - window_offset[0] - mouse_pointer_size//2,
                                              pygame.mouse.get_pos()[1] - window_offset[1] - mouse_pointer_size//2])

        fps_counter.draw_text(f"{str(clock.get_fps())[:4]}")
        window.image.blit(fps_counter.image, fps_counter.rect)

        # window
        screen.blit(window.image, window.rect)

        if active_piece is not None:
            screen.blit(active_piece.image, [pygame.mouse.get_pos()[0] - active_piece.rect.width // 2,
                                             pygame.mouse.get_pos()[1] - active_piece.rect.height // 2])

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    game(pygame.display.set_mode((1, 1), pygame.RESIZABLE))
    pygame.quit()
