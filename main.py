import pygame
import pygame.freetype
import pygame_widgets
import math
import time
import sys
import _collections
import random
import matplotlib.pyplot as plt
import numpy as np
Vector = pygame.math.Vector2

# initialize pygame
pygame.init()
FPS = 100  # frames per second
fps_clock = pygame.time.Clock()
# set up the window
WIDTH = 1280
HEIGHT = 900
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

free_way = 0
previous_time = time.perf_counter()
collisions = 0
mean_freeway = []
freq_of_collisons = []
number_of_atoms = []
number_of_ticks = []

class Atomic_Container(pygame.sprite.Sprite):
    def __init__(self, basic_atom):
        self.atom = basic_atom
        self.atoms = [Atom(self.atom.radius, self.atom.mass)]

    def instantia_atoms(self, amount):
        for i in range(0, amount):
            self.atoms.append(Atom(self.atom.radius, self.atom.mass))
        self.atoms.append(SpecialAtom(self.atom.radius, self.atom.mass))

    def print_atoms_position(self):
        print(self.atoms[-1].speed)


    def draw_atoms(self, surface):
        surface.fill((198, 210, 209))
        i = 0
        for atom in self.atoms:
            pygame.draw.circle(surface, RED, (int(atom.position.x),  int(atom.position.y)), atom.radius)
            i += 1
            if i == len(self.atoms) - 1:
                break
        pygame.draw.circle(surface, BLUE, (int(self.atoms[-1].position.x), int(self.atoms[-1].position.y)), atom.radius)

    def move_atom(self):
        for atom in self.atoms:
            atom.position += atom.speed

    '''def collision_with_atoms(self):
        for i in range(0, len(self.atoms)):
            for j in range(i, len(self.atoms)):
                atom_1 = self.atoms[i]
                atom_2 = self.atoms[j]
                if atom_1 != atom_2 and atom_1.position.distance_to(atom_2.position) <= (2*atom_1.radius + 1):
                    #self.move_atom_to_avoid_stacking(atom_1, atom_2)
                    atom_1.speed = atom_1.speed.reflect(atom_1.speed)
                    atom_2.speed = atom_2.speed.reflect(atom_2.speed)'''

    '''def move_atom_to_avoid_stacking(self, atom_1, atom_2):
        x_diff = atom_1.position.x - atom_2.position.x
        y_diff = atom_1.position.y - atom_2.position.y
        if x_diff > 0:
            atom_1.position.x -= x_diff
        elif x_diff < 0:
            atom_1.position.x += x_diff
        if y_diff > 0:
            atom_1.position.y -= y_diff
        elif y_diff < 0:
            atom_1.position.y += y_diff'''

    def collision_wth_atoms_v2_utility(self, atom_1, atom_2):\
        ### Dlugosc wektora predkosci pierwszego atomu ###
        atom_1_speed = math.sqrt((atom_1.speed.x ** 2) + (atom_1.speed.y ** 2))
        ### Roznica odlegosci pomiedzy srodkami atomu na osi X
        x_diff = -(atom_1.position.x - atom_2.position.x)
        ### Roznica odlegosci pomiedzy srodkami atomu na osi Y
        y_diff = -(atom_1.position.y - atom_2.position.y)
        if x_diff > 0:
            ### Kat zderzenia pomiedzy atomami wylicznay za pomoca arcusatangensa pomiedzy wartosciami
            angle = math.degrees(math.atan(y_diff / x_diff))
            x_speed = -atom_1_speed * math.cos(math.radians(angle))
            y_speed = -atom_1_speed * math.sin(math.radians(angle))
        elif x_diff < 0:
            if y_diff > 0:
                angle = 180 + math.degrees(math.atan(y_diff / x_diff))
                x_speed = -atom_1_speed * math.cos(math.radians(angle))
                y_speed = -atom_1_speed * math.sin(math.radians(angle))
            elif y_diff < 0:
                angle = -180 + math.degrees(math.atan(y_diff / x_diff))
                x_speed = -atom_1_speed * math.cos(math.radians(angle))
                y_speed = -atom_1_speed * math.sin(math.radians(angle))
        elif x_diff == 0:
            if y_diff > 0:
                angle = -90
            else:
                angle = 90
            x_speed = atom_1_speed * math.cos(math.radians(angle))
            y_speed = atom_1_speed * math.sin(math.radians(angle))
        elif y_diff == 0:
            if x_diff < 0:
                angle = 0
            else:
                angle = 180
            x_speed = atom_1_speed * math.cos(math.radians(angle))
            y_speed = atom_1_speed * math.sin(math.radians(angle))
        atom_1.speed.x = x_speed
        atom_1.speed.y = y_speed

    def collision_wth_atoms_v2(self):
        global free_way
        global collisions
        for atom_1 in self.atoms:
            for atom_2 in self.atoms:
                if not(atom_1 is atom_2):
                    if math.sqrt(((atom_1.position.x - atom_2.position.x) ** 2) + ((atom_1.position.y - atom_2.position.y) ** 2)) <= (atom_1.radius + atom_2.radius):
                        if atom_1 is self.atoms[-1]:
                            collisions += 1
                            self.calculate_freeway(self.atoms[-1])
                        self.collision_wth_atoms_v2_utility(atom_1, atom_2)

    def collision_with_container(self, container):
        for atom in self.atoms:
            if atom.position.x <= atom.radius or atom.position.x >= container.width - atom.radius:
                atom.speed.x *= -1
            if atom.position.y <= atom.radius or atom.position.y >= container.height - atom.radius:
                atom.speed.y *= -1

    def calculate_freeway(self, atom):
        global  free_way
        global previous_time
        global collisions
        current_time = time.perf_counter()
        free_way += ((atom.speed * (current_time-previous_time)).length())
        previous_time = time.perf_counter()


class Atom():

    def __init__(self, radius, mass):
        self.radius = radius
        self.mass = mass
        self.position = Vector(random.randint(radius, 800-radius), random.randint(radius, 800-radius))
        self.speed = Vector(2*(random.random()+2.0), 2*(random.random()+2.0))

class SpecialAtom(Atom):
    def __init__(self, radius, mass):
        self.radius = radius
        self.mass = mass
        self.position = Vector(radius, radius)
        self.speed = Vector(2*(random.random()+2.0), 2*(random.random()+2.0))

class Container(pygame.sprite.Sprite):

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((198, 210, 209))
        pygame.draw.rect(self.image, (140, 163, 163), ((0, 0), (self.width, self.height)), 10)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)


def Simulation(fps, number_of_atoms):
    global mean_freeway, freq_of_collisons
    all_sprites = pygame.sprite.Group()
    basic_atom = Atom(10, 1)
    container = Container(80 * basic_atom.radius, 80 * basic_atom.radius)
    atom_container = Atomic_Container(basic_atom)
    atom_container.instantia_atoms(number_of_atoms)
    all_sprites.add(container)
    t0 = time.perf_counter()

    ### GAME LOOP ###
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit()
        atom_container.move_atom()
        atom_container.collision_wth_atoms_v2()
        atom_container.collision_with_container(container)
        atom_container.draw_atoms(container.image)
        all_sprites.update()
        all_sprites.draw(DISPLAY)
        pygame.display.update()
        fps_clock.tick(fps)
        if  time.perf_counter() - t0 > 10:
            try:
                mean_freeway.append(free_way / collisions)
            except ZeroDivisionError:
                mean_freeway.append(0)
            freq_of_collisons.append(collisions / time.perf_counter())
            return 0

def main():
    for fps in range(20, 70, 20):
        for atoms in range(10, 300, 10):
                number_of_atoms.append((atoms))
                number_of_ticks.append((fps))
                Simulation(fps, atoms)
                print(mean_freeway, number_of_atoms)
                plt.plot(number_of_atoms, mean_freeway)
                #plt.plot(number_of_atoms, freq_of_collisons)
                plt.show()

if __name__ == '__main__':
    main()
