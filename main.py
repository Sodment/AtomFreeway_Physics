import pygame as game
import pygame.freetype
import pygame_widgets
import cmath as cmath
import time as time
import sys as system
import _collections


def rysuj_ramke(surface, szerokosc , wysokosc):
    game.draw.rect(surface, (140, 163, 163), (30, 30, szerokosc, wysokosc), 5)
    surface.fill((198, 210, 209), (35, 35, szerokosc-10, wysokosc-10))


def rysuj_okno(szerokosc, wysokosc):
    screen = game.display.set_mode((szerokosc, wysokosc))
    screen.fill((72, 79, 79))
    return screen


def main():
    game.init()
    screen = rysuj_okno(1280, 820)
    font = game.freetype.SysFont(None, 32)
    clock = game.time.Clock()
    rysuj_ramke(screen, 580, 720)
    slider = pygame_widgets.Slider(screen, 100, 100, 800, 40, min=0, max=99, step=1)


### Wychodzenie z gry ###
    while True:
        events = game.event.get()
        for e in events:
            if e.type == game.QUIT:
                return 0
        slider.listen(events)
        slider.draw()
        game.display.update()

if __name__ == '__main__':
    main()
