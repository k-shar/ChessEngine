import pygame
from pygame import freetype
import engine_config


class ScaleSurface(pygame.sprite.Sprite):
    def __init__(self, name, ratio, alignment, padding):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        self.name = name
        self.color_set = engine_config.default_theme
        self.color = self.color_set[name]

        self.ratio = ratio
        self.alignment = alignment
        self.padding = padding  # float 0-1 determining how much of the parent surf is filled

    def setcolor(self, color):
        self.color = color
        self.image.fill(self.color)

    def resize(self, parent):
        self.color = self.color_set[self.name]
        self.image.fill(self.color)

        # -- create padding between outer and inner --
        # create a shrunk outer surface to use instead, so when the inner surface is expanded there will be some gap
        shrunk_outer_surf = pygame.transform.scale(parent, (int(parent.get_width() * self.padding),
                                                            int(parent.get_height() * self.padding)))

        # -- expand to fill shrunk_outer_surf --
        max_size = list(shrunk_outer_surf.get_size())
        i = 0
        test_size = [self.ratio[0] * i, self.ratio[1] * i]
        # while test_size is not overflowing max_size, increase test_size
        while not (test_size[0] > max_size[0]) and not (test_size[1] > max_size[1]):
            i += 1  # increase the test size
            test_size = [self.ratio[0] * i, self.ratio[1] * i]

        # rollback last attempted scale up so we are no longer overflowing max_size
        test_size = [test_size[0] - self.ratio[0], test_size[1] - self.ratio[1]]
        # set image to the new scaled dimensions
        self.image = pygame.transform.scale(self.image, test_size)

        # -- center smaller surface --
        self.rect = self.image.get_rect()
        self.rect.centerx = int(parent.get_width() * self.alignment[0])
        self.rect.centery = int(parent.get_height() * self.alignment[1])


class TextSurface(ScaleSurface):
    def __init__(self, color, ratio, alignment, padding, text, text_size, text_color, text_loc):
        super().__init__(color, ratio, alignment, padding)

        self.text_color = engine_config.default_theme[text_color]
        self.active_text = text
        self.text_size = text_size
        self.text_loc = text_loc

        self.text_surf, self.text_rect = None, None
        self.parent = None

    def setcolor(self, color):
        super().setcolor(color)
        self.draw_text(self.active_text)

    def resize(self, parent):
        super().resize(parent)
        # draw text over resized surface
        self.draw_text(self.active_text)

    def draw_text(self, text):
        super().setcolor(self.color)
        # create font
        font = pygame.freetype.SysFont("Consolas", self.image.get_height())
        # set height of text, special case for (0, 0) as text size must be non zero
        size = 1 if self.image.get_size() == (0, 0) else self.image.get_height() * self.text_size
        # render font
        self.text_surf, self.text_rect = font.render(text, fgcolor=self.text_color, size=size)

        center = [self.image.get_rect().centerx, self.image.get_rect().centery]
        center[0] *= self.text_loc[0]
        center[1] *= self.text_loc[1]
        self.image.blit(self.text_surf, self.text_surf.get_rect(center=center))


class Button(TextSurface):
    def __init__(self, color, ratio, alignment, padding, text, text_size):
        super().__init__(color, ratio, alignment, padding, text, text_size, "TEXT", (1, 1))
        self.hovered, self.clicked = False, False

    def hover(self, is_hovered):
        self.hovered = is_hovered

        if is_hovered:
            self.setcolor(self.color_set["HOVERED"])
        else:
            self.setcolor(self.color_set[self.name])
        super().draw_text(self.active_text)

    def click(self, is_clicked):
        self.clicked = is_clicked


class ResetButton(Button):
    def __init__(self, color, ratio, alignment, padding, text, text_size,):
        super().__init__(color, ratio, alignment, padding, text, text_size)
        self.hover_color_name = "RESET"

    def hover(self, is_hovered):
        if is_hovered:
            self.setcolor(self.color_set["RESET"])
            self.text_color = self.color_set["BORDER"]
        else:
            self.setcolor(self.color_set["BORDER"])
            self.text_color = self.color_set["TEXT"]
        super().draw_text(self.active_text)

    def click(self, is_clicked):
        print("reset!")


class ColorThemeButton(Button):
    def __init__(self, alignment, button_name, color_theme):
        super().__init__("BUTTON", (5, 3), alignment, 0.22, button_name, 0.4)

        self.color_theme = color_theme
        self.button_name = button_name  # primary text

    def click(self, clicked):
        # swap text
        if clicked:
            self.active_text = "√"
            self.text_size = 0.6
            super().hover(True)
        else:
            self.active_text = self.button_name
            self.text_size = 0.4
        super().click(clicked)
        return self.color_theme


class HintsToggle(Button):
    def __init__(self, alignment, text):
        super().__init__("BUTTON", (5, 1), alignment, 0.9, text, 0.6)

        self.color = engine_config.blue_theme["BUTTON"]
        self.text_color = engine_config.blue_theme["TEXT"]

        self.checkbox = Button("BORDER", (1, 1), (0.9, 0.5), 0.7, "x", 0.9)
        self.parent = None

        self.is_clicked = False

    def resize(self, parent):
        super().resize(parent)
        self.parent = parent
        self.checkbox.resize(self.image)
        self.draw_checkbox()

    def draw_checkbox(self):
        self.image.blit(self.checkbox.image, self.checkbox.rect)

    def hover(self, is_hovered):
        super().hover(is_hovered)
        self.image.blit(self.checkbox.image, self.checkbox.rect)

    def click(self, is_clicked):
        self.is_clicked = is_clicked
        if is_clicked:
            self.checkbox.active_text = "√"
        else:
            self.checkbox.active_text = "x"
        self.checkbox.draw_text(self.checkbox.active_text)
