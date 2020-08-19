import pygame
import pygame.freetype
import pygame_widgets
import cmath
import time
import sys
import _collections
Vector = pygame.math.Vector2

# initialize pygame
pygame.init()
FPS = 60  # frames per second
fps_clock = pygame.time.Clock()
# set up the window
WIDTH = 1280
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ATOMOWO!')
FONT = pygame.font.Font(None, 32)
# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Atom(pygame.sprite.Sprite):

    def __init__(self, radius, mass, surface, width, heigth):
        self.atom_image = pygame.Surface((radius, radius))
        pygame.draw.circle(surface, (157, 123, 133), (width, heigth), radius)
        self.original_atom = self.atom_image

class Container(pygame.sprite.Sprite):

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((157, 123, 133))
        pygame.draw.rect(self.image, (140, 163, 163), ((0, 0), (width, height)), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//3, HEIGHT//2)
        self.position = (30, 30)




def main():
    all_sprites = pygame.sprite.Group()
    container = Container(600, 600)
    all_sprites.add(container)
    ### GAME LOOP ###
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return 0
        DISPLAY.fill((140, 163, 163))
        all_sprites.update()
        all_sprites.draw(DISPLAY)
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()
