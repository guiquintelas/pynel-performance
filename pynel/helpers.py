from pynel.settings import *


def draw_text(tela, text, y, small=False, x=50.0, no_pad=False, color=WHITE):
    if small:
        textsurface = small_fonte.render(str(text), False, color)
        if not no_pad:
            x += 40
    else:
        textsurface = fonte.render(str(text), False, color)

    tela.blit(textsurface, (x, y))


def get_height(index):
    return init_height + pad_mod * float(index)


def text_width(text):
    return small_fonte.render(text, False, (255, 255, 255)).get_width()


class Pynel:
    def __init__(self, nome):
        self.index = 0
        self.nome = nome
        self.sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))
        self.init_height = init_height
        self.use_update = True

    def update(self, eventos):
        pass

    def draw(self):
        pass

    def draw_geral(self):
        pass

    def next_height(self, same=False, small=False):
        y = self.init_height + pad_mod * self.index

        if not same:
            if small:
                self.index += .5
            else:
                self.index += 1
        return y

    def add_pad(self, pad):
        self.index += pad

    def use_init_height(self, enable):
        if enable:
            self.init_height = init_height
        else:
            self.init_height = 0
