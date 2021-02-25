import pygame
import os
import sys
from random import shuffle
from math import sqrt


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey((255, 255, 255))
    return image


tile_width = tile_height = 50


def can_move(direction, position, test_map):
    if direction == 3:
        return test_map[position[1] - 1][position[0]] != '#'
    elif direction == 0:
        return test_map[position[1]][position[0] - 1] != '#'
    elif direction == 1:
        return test_map[position[1] + 1][position[0]] != '#'
    elif direction == 2:
        return test_map[position[1]][position[0] + 1] != '#'


class Ghosts:
    def __init__(self):
        self.direction = -1
        self.moved = 0
        self.in_cell = True

    def moving(self, ghost_map):
        if self.in_cell:
            self.in_cell = False
            x_distance = self.target[0] - self.position[0]
            y_distance = self.target[1] - self.position[1]
            choices = [-1, -1, -1, -1]

            if abs(x_distance) > abs(y_distance):  # horizontal 1st
                if x_distance > 0:  # right 1st
                    choices[0] = 2
                    choices[3] = 0
                elif x_distance < 0:  # left 1st
                    choices[0] = 0
                    choices[3] = 2

                if y_distance > 0:  # down 2nd
                    choices[1] = 1
                    choices[2] = 3
                elif y_distance < 0:  # up 2nd
                    choices[1] = 3
                    choices[2] = 1
                else:  # y_distance == 0
                    choices[1] = 1
                    choices[2] = 3

            elif abs(y_distance) >= abs(x_distance):  # vertical 1st
                if y_distance > 0:  # down 1st
                    choices[0] = 1
                    choices[3] = 3
                elif y_distance < 0:  # up 1st
                    choices[0] = 3
                    choices[3] = 1

                if x_distance > 0:  # right 2nd
                    choices[1] = 2
                    choices[2] = 0
                elif x_distance < 0:  # left 2nd
                    choices[1] = 0
                    choices[2] = 2
                else:  # x_distance == 0
                    choices[1] = 2
                    choices[2] = 0
            if self.is_blue:
                shuffle(choices)
            for i, x in enumerate(choices):
                if x != -1 and can_move(x, self.position, ghost_map) and abs(self.direction - x) != 2:
                    self.direction = choices[i]
                    break
        else:
            if self.direction == 0:
                self.rect.x -= 1
            elif self.direction == 3:
                self.rect.y -= 1
            elif self.direction == 2:
                self.rect.x += 1
            elif self.direction == 1:
                self.rect.y += 1
            self.moved += 1

            if self.moved == 20:
                if self.direction == 0:
                    self.position[0] -= 1
                elif self.direction == 3:
                    self.position[1] -= 1
                elif self.direction == 2:
                    self.position[0] += 1
                elif self.direction == 1:
                    self.position[1] += 1
                self.moved = 0
                self.in_cell = True


class RedGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, red_positions, red_directions):
        super().__init__()
        self.image = pygame.transform.scale(load_image('RedGhost.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = red_positions[0] * 20
        self.rect.y = red_positions[1] * 20
        self.direction = red_directions
        self.target = []
        self.position = red_positions
        self.moved = 0
        self.in_cell = True
        self.is_blue = False

    def update(self, red_pacman_position, mode, red_map):
        if mode == 'chase':
            self.target = red_pacman_position
        else:
            self.target = [25, 0]
        Ghosts.moving(self, red_map)
        return self.position

    def change_direction(self):
        self.direction = (self.direction + 2) % 4
        self.moved = 20 - self.moved
        if self.direction == 3:
            self.position[1] += 1
        elif self.direction == 1:
            self.position[1] -= 1
        elif self.direction == 0:
            self.position[0] += 1
        elif self.direction == 2:
            self.position[0] -= 1


class PinkGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, pink_positions, pink_directions):
        super().__init__()
        self.image = pygame.transform.scale(load_image('PinkGhost.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pink_positions[0] * 20
        self.rect.y = pink_positions[1] * 20
        self.direction = pink_directions
        self.target = []
        self.position = pink_positions
        self.moved = 0
        self.in_cell = True
        self.is_blue = False

    def update(self, pink_pacman_position, mode, pink_map, pink_pacman_direction):
        if mode == 'chase':
            if pink_pacman_direction == 0:
                self.target = [pink_pacman_position[0] - 4, pink_pacman_position[1]]
            elif pink_pacman_direction == 1:
                self.target = [pink_pacman_position[0], pink_pacman_position[1] + 4]
            elif pink_pacman_direction == 2:
                self.target = [pink_pacman_position[0] + 4, pink_pacman_position[1]]
            elif pink_pacman_direction == 3:
                self.target = [pink_pacman_position[0], pink_pacman_position[1] - 4]
        else:
            self.target = [0, 0]
        Ghosts.moving(self, pink_map)

    def change_direction(self):
        self.direction = (self.direction + 2) % 4
        self.moved = 20 - self.moved
        if self.direction == 3:
            self.position[1] += 1
        elif self.direction == 1:
            self.position[1] -= 1
        elif self.direction == 0:
            self.position[0] += 1
        elif self.direction == 2:
            self.position[0] -= 1


class BlueGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, blue_positions, blue_directions):
        super().__init__()
        self.image = pygame.transform.scale(load_image('BlueGhost.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = blue_positions[0] * 20
        self.rect.y = blue_positions[1] * 20
        self.direction = blue_directions
        self.target = []
        self.position = blue_positions
        self.moved = 0
        self.in_cell = True
        self.is_blue = False

    def update(self, blue_pacman_position, mode, blue_map, blue_red_position, blue_pacman_direction):
        if mode == 'chase':
            self.target = [0, 0]
            target1 = blue_red_position
            if blue_pacman_direction == 0:
                target2 = [blue_pacman_position[0] - 2, blue_pacman_position[1]]
            elif blue_pacman_direction == 1:
                target2 = [blue_pacman_position[0], blue_pacman_position[1] + 2]
            elif blue_pacman_direction == 2:
                target2 = [blue_pacman_position[0] + 2, blue_pacman_position[1]]
            else:
                target2 = [blue_pacman_position[0], blue_pacman_position[1] - 2]
            self.target = [target2[0] * 2 - target1[0], target2[1] * 2 - target1[1]]
        else:
            self.target = [25, 34]
        Ghosts.moving(self, blue_map)

    def change_direction(self):
        self.direction = (self.direction + 2) % 4
        self.moved = 20 - self.moved
        if self.direction == 3:
            self.position[1] += 1
        elif self.direction == 1:
            self.position[1] -= 1
        elif self.direction == 0:
            self.position[0] += 1
        elif self.direction == 2:
            self.position[0] -= 1


class BrownGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, brown_positions, brown_directions):
        super().__init__()
        self.image = pygame.transform.scale(load_image('BrownGhost.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = brown_positions[0] * 20
        self.rect.y = brown_positions[1] * 20
        self.direction = brown_directions
        self.target = []
        self.position = brown_positions
        self.moved = 0
        self.in_cell = True
        self.is_blue = False

    def update(self, brown_pacman_position, mode, brown_map):
        if mode == 'chase':
            range_from_pacman = sqrt((brown_pacman_position[0] - self.position[0]) ** 2 + (brown_pacman_position[1] -
                                                                                            self.position[1]) ** 2)
            if range_from_pacman <= 8:
                self.target = [0, 34]
            else:
                self.target = brown_pacman_position
        else:
            self.target = [0, 34]
        Ghosts.moving(self, brown_map)
        return self.position

    def change_direction(self):
        self.direction = (self.direction + 2) % 4
        self.moved = 20 - self.moved
        if self.direction == 3:
            self.position[1] += 1
        elif self.direction == 1:
            self.position[1] -= 1
        elif self.direction == 0:
            self.position[0] += 1
        elif self.direction == 2:
            self.position[0] -= 1


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def start_screen():
    intro_text = ["PacMan",
                  "Стрелками мыши управляйте пакманом, собирайте точки.",
                  "Избегайте призраков, они могут съесть вас. При сборе",
                  "больших точек вы на короткое время сможете есть призраков. Удачи!"]

    fon = pygame.transform.scale(load_image('Pacman_Image.png'), (580, 720))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    start_running = True
    while start_running:
        for start_event in pygame.event.get():
            if start_event.type == pygame.QUIT:
                pygame.quit()
                start_running = False
                return False
            elif start_event.type == pygame.MOUSEBUTTONDOWN or start_event.type == pygame.KEYDOWN:
                start_running = False
                return True
        if start_running:
            pygame.display.flip()


def generate_level(level, color):
    for y in range(len(level)):
        for x in range(len(level[y])):
            pygame.draw.rect(screen, (0, 0, 0), (x * 20, y * 20, x * 20 + 19, y * 20 + 19), 0)
            if level[y][x] == '.':
                pass
            elif level[y][x] == '*':
                pygame.draw.line(screen, (255, 255, 255), (x * 20 + 9, y * 20 + 9), (x * 20 + 11, y * 20 + 9))
                pygame.draw.line(screen, (255, 255, 255), (x * 20 + 9, y * 20 + 10), (x * 20 + 11, y * 20 + 10))
                pygame.draw.line(screen, (255, 255, 255), (x * 20 + 9, y * 20 + 11), (x * 20 + 11, y * 20 + 11))
            elif level[y][x] == 'E':
                pygame.draw.circle(screen, (255, 255, 255), (x * 20 + 11, y * 20 + 10), 7)
            elif level[y][x] == '#':
                if x == len(level[y]) - 1:
                    x = -1
                if y == len(level) - 1:
                    y = -1
                if level[y][x - 1] != '#':
                    pygame.draw.line(screen, color, (x * 20, y * 20), (x * 20, y * 20 + 19))
                if level[y][x + 1] != '#':
                    pygame.draw.line(screen, color, (x * 20 + 19, y * 20), (x * 20 + 19, y * 20 + 19))
                if level[y - 1][x] != '#':
                    pygame.draw.line(screen, color, (x * 20, y * 20), (x * 20 + 19, y * 20))
                if level[y + 1][x] != '#':
                    pygame.draw.line(screen, color, (x * 20, y * 20 + 19), (x * 20 + 19, y * 20 + 19))


pygame.init()
running = True
directions = ['left', 'down', 'right', 'up']
clock = pygame.time.Clock()
pacman_direction = 2
pink_direction = 2
brown_direction = 0
blue_direction = 2
red_direction = 0
pacman_position = [14, 26]
red_position = [13, 14]
pink_position = [14, 14]
blue_position = [11, 17]
brown_position = [15, 17]
screen = pygame.display.set_mode((560, 720))
level_number = 1
dots = 0
base_map = load_level('level1.txt')
pacman_map = load_level('pacman_level1.txt')
n = start_screen()
lives = 3
ghosts = Ghosts
ghost_mode = 'scatter'
mode_timer = pygame.time.Clock()
mode_timer.tick()
alternating_mods = [[7, 20, 7, 20, 5, 20, 5], [7, 20, 7, 20, 5, 1033, 1], [5, 20, 5, 20, 1, 1037, 1]]
red_ghost = pygame.sprite.Group()
red_ghost.add(RedGhost(red_position, red_direction))
pink_ghost = pygame.sprite.Group()
pink_ghost.add(PinkGhost(pink_position, pink_direction))
blue_ghost = pygame.sprite.Group()
blue_ghost.add(BlueGhost(blue_position, blue_direction))
brown_ghost = pygame.sprite.Group()
brown_ghost.add(BrownGhost(brown_position, brown_direction))
clock.tick()
required_dots = [244, 262, 242, 262, 250, 266, 260, 260, 232]
mode_time_number = 0
mode_time = 0
colors = ['blue', (0, 255, 255), 'yellow', 'purple', 'red', (50, 50, 150), 'mediumvioletred', 'green', 'blue']
while running and n:
    screen.fill('black')
    generate_level(pacman_map, colors[level_number - 1])
    red_ghost.draw(screen)
    pink_ghost.draw(screen)
    blue_ghost.draw(screen)
    brown_ghost.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                pacman_direction = 1
            if event.key == pygame.K_UP:
                pacman_direction = 3
            if event.key == pygame.K_LEFT:
                pacman_direction = 0
            if event.key == pygame.K_RIGHT:
                pacman_direction = 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    clock.tick(60)
    for red_ghost1 in red_ghost:
        red_position = red_ghost1.update(pacman_position, ghost_mode, base_map)
    pink_ghost.update(pacman_position, ghost_mode, base_map, pacman_direction)
    blue_ghost.update(pacman_position, ghost_mode, base_map, red_position, pacman_direction)
    brown_ghost.update(pacman_position, ghost_mode, base_map)
    if dots == required_dots[level_number - 1]:
        level_number += 1
        base_map = load_level('level' + str(level_number) + '.txt')
        pacman_map = load_level('pacman_level' + str(level_number) + '.txt')
        lives = 3
        mode_time_number = 0
        dots = 0
    if level_number == 1:
        mode_times = alternating_mods[0]
    elif level_number < 5:
        mode_times = alternating_mods[1]
    else:
        mode_times = alternating_mods[2]
    mode_time += 1
    if mode_time_number != 7:
        if mode_time >= mode_times[mode_time_number] * 40:
            mode_time_number += 1
            mode_time = 0
            if mode_time_number % 2 == 0:
                ghost_mode = 'scatter'
            else:
                ghost_mode = 'chase'
            for i in red_ghost:
                i.change_direction()
            for i in pink_ghost:
                i.change_direction()
            for i in blue_ghost:
                i.change_direction()
            for i in brown_ghost:
                i.change_direction()
    else:
        ghost_mode = 'chase'
    pygame.display.flip()
pygame.quit()