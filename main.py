import pygame
import pygame.freetype
import pygame_widgets
import math
import time
import sys
import _collections
import random
Vector = pygame.math.Vector2

# initialize pygame
pygame.init()
FPS = 60  # frames per second
fps_clock = pygame.time.Clock()
# set up the window
WIDTH = 1280
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY.fill((72, 79, 79))
pygame.display.set_caption('ATOMOWO!')
FONT = pygame.font.Font(None, 32)
# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Atomic_Container(pygame.sprite.Sprite):
    def __init__(self):
        self.atoms = []

    def instantia_atoms(self, amount):
        for i in range(amount):
            self.atoms.append(Atom(10,1))

    def draw_atoms(self, surface):
        surface.fill((198, 210, 209))
        for atom in self.atoms:
            pygame.draw.circle(surface, (157, 123, 133), (int(atom.position.x),  int(atom.position.y)), atom.radius)

    def move_atom(self):
        for atom in self.atoms:
            atom.position += atom.speed

    def collisions(self, container):
        for atom in self.atoms:
            if atom.position.x < atom.radius or atom.position.x > container.width - atom.radius:    atom.speed.x *= -1
            if atom.position.y < atom.radius or atom.position.y > container.height - atom.radius:    atom.speed.y *= -1
        for i in range(0, len(self.atoms)):
            for j in range(i, len(self.atoms)):
                atom_1 = self.atoms[i]
                atom_2 = self.atoms[j]
                if atom_1 != atom_2 and atom_1.position.distance_to(atom_2.position) <= (2*atom_1.radius):
                    atom_1.position += Vector(2 * atom_1.radius - atom_1.position.distance_to(atom_2.position))
                    atom_1.speed = atom_1.speed.reflect(atom_1.speed)
                    atom_2.speed = atom_2.speed.reflect(atom_2.speed)



class Atom():

    def __init__(self, radius, mass):
        self.radius = radius
        self.position = Vector(random.randint(radius, 600-radius), random.randint(radius, 720-radius))
        self.speed = Vector(0.5*(random.random()+1.0), 0.5*(random.random()+1.0))

class Container(pygame.sprite.Sprite):

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill((198, 210, 209))
        pygame.draw.rect(self.image, (140, 163, 163), ((0, 0), (width, height)), 10)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)




def main():
    all_sprites = pygame.sprite.Group()
    container = Container(600, 720)
    atom_container = Atomic_Container()
    atom_container.instantia_atoms(100)
    all_sprites.add(container)

    ### GAME LOOP ###
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return 0
        atom_container.move_atom()
        atom_container.collisions(container)
        atom_container.draw_atoms(container.image)
        all_sprites.update()
        all_sprites.draw(DISPLAY)
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()
