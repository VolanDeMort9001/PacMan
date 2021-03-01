import pygame
import os
import sys
from random import shuffle
from math import sqrt
from random import randint

def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(image.get_at((0, 0)))
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

            if abs(x_distance) > abs(y_distance):
                if x_distance > 0:
                    choices[0] = 2
                    choices[3] = 0
                elif x_distance < 0:
                    choices[0] = 0
                    choices[3] = 2

                if y_distance > 0:
                    choices[1] = 1
                    choices[2] = 3
                elif y_distance < 0:
                    choices[1] = 3
                    choices[2] = 1
                else:
                    choices[1] = 1
                    choices[2] = 3

            elif abs(y_distance) >= abs(x_distance):
                if y_distance > 0:
                    choices[0] = 1
                    choices[3] = 3
                elif y_distance < 0:
                    choices[0] = 3
                    choices[3] = 1

                if x_distance > 0:
                    choices[1] = 2
                    choices[2] = 0
                elif x_distance < 0:
                    choices[1] = 0
                    choices[2] = 2
                else:
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
            if self.moved >= 20:
                if self.direction == 0:
                    self.position[0] -= 1
                elif self.direction == 3:
                    self.position[1] -= 1
                elif self.direction == 2:
                    self.position[0] += 1
                elif self.direction == 1:
                    self.position[1] += 1
                self.moved -= 20
                self.in_cell = True


class RedGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, red_positions, red_directions):
        super().__init__()
        self.image = load_image('RedGhost.png')
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
            self.image = load_image('RedGhost.png')
            self.target = red_pacman_position
        elif mode == 'scatter':
            self.image = load_image('RedGhost.png')
            self.target = [25, 0]
        else:
            self.image = load_image('ScaredGhost.png')
            self.target = [randint(0, 27), randint(0, 35)]
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
        return self.position

    def start_pos(self):
        self.position = [13, 14]
        self.rect.x = 260
        self.rect.y = 280
        self.moved = 0
        self.direction = 0


class PinkGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, pink_positions, pink_directions):
        super().__init__()
        self.image = load_image('PinkGhost.png')
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
            self.image = load_image('PinkGhost.png')
            if pink_pacman_direction == 0:
                self.target = [pink_pacman_position[0] - 4, pink_pacman_position[1]]
            elif pink_pacman_direction == 1:
                self.target = [pink_pacman_position[0], pink_pacman_position[1] + 4]
            elif pink_pacman_direction == 2:
                self.target = [pink_pacman_position[0] + 4, pink_pacman_position[1]]
            elif pink_pacman_direction == 3:
                self.target = [pink_pacman_position[0], pink_pacman_position[1] - 4]
        elif mode == 'scatter':
            self.image = load_image('PinkGhost.png')
            self.target = [0, 0]
        else:
            self.image = load_image('ScaredGhost.png')
            self.target = [randint(0, 27), randint(0, 35)]
        Ghosts.moving(self, pink_map)
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
        return self.position

    def start_pos(self):
        self.position = [14, 14]
        self.rect.x = 280
        self.rect.y = 280
        self.moved = 0
        self.direction = 2

class BlueGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, blue_positions, blue_directions):
        super().__init__()
        self.image = load_image('BlueGhost.png')
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
            self.image = load_image('BlueGhost.png')
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
            self.target = [target1[0] * 2 - target2[0], target1[1] * 2 - target2[1]]
        elif mode == 'scatter':
            self.image = load_image('BlueGhost.png')
            self.target = [25, 34]
        else:
            self.image = load_image('ScaredGhost.png')
            self.target = [randint(0, 27), randint(0, 35)]
        Ghosts.moving(self, blue_map)
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
        return self.position

    def start_pos(self):
        self.position = [12, 14]
        self.rect.x = 240
        self.rect.y = 280
        self.moved = 0
        self.direction = 0


class BrownGhost(pygame.sprite.Sprite, Ghosts):
    def __init__(self, brown_positions, brown_directions):
        super().__init__()
        self.image = load_image('BrownGhost.png')
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
            self.image = load_image('BrownGhost.png')
            range_from_pacman = sqrt((brown_pacman_position[0] - self.position[0]) ** 2 + (brown_pacman_position[1] -
                                                                                            self.position[1]) ** 2)
            if range_from_pacman <= 8:
                self.target = [0, 34]
            else:
                self.target = brown_pacman_position
        elif mode == 'scatter':
            self.image = load_image('BrownGhost.png')
            self.target = [0, 34]
        else:
            self.image = load_image('ScaredGhost.png')
            self.target = [randint(0, 27), randint(0, 35)]
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
        return self.position

    def start_pos(self):
        self.position = [15, 14]
        self.rect.x = 300
        self.rect.y = 280
        self.moved = 0
        self.direction = 2


class PacMan(pygame.sprite.Sprite):
    def __init__(self, color_of_pacman):
        super().__init__()
        self.image_classic = load_image(color_of_pacman + 'PacMan_classic.png')
        self.image0 = load_image(color_of_pacman + 'PacMan0.png')
        self.image1 = load_image(color_of_pacman + 'PacMan1.png')
        self.image2 = load_image(color_of_pacman + 'PacMan2.png')
        self.image3 = load_image(color_of_pacman + 'PacMan3.png')
        self.marker = 0
        self.image = self.image_classic
        self.position = [14, 26]
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 20
        self.rect.y = self.position[1] * 20
        self.direction = 2
        self.required_direction = 2
        self.x_moved = 0
        self.y_moved = 0
        self.dot_is_putted = False
        self.is_blue = False

    def changing(self):
        self.marker = 1 - self.marker
        if self.marker == 0:
            self.image = self.image_classic
        else:
            if self.direction == 0:
                self.image = self.image0
            elif self.direction == 1:
                self.image = self.image1
            elif self.direction == 2:
                self.image = self.image2
            elif self.direction == 3:
                self.image = self.image3

    def update(self):
        self.dot_is_putted = False
        self.is_blue = False
        if can_move(self.direction, self.position, base_map):
            if self.direction == 0:
                self.rect.x -= 1
                self.x_moved -= 1
            elif self.direction == 1:
                self.rect.y += 1
                self.y_moved += 1
            elif self.direction == 2:
                self.rect.x += 1
                self.x_moved += 1
            elif self.direction == 3:
                self.rect.y -= 1
                self.y_moved -= 1
        if self.x_moved == -20:
            self.position[0] -= 1
            self.x_moved = 0
        elif self.x_moved == 20:
            self.position[0] += 1
            self.x_moved = 0
        if self.y_moved == -20:
            self.position[1] -= 1
            self.y_moved = 0
        elif self.y_moved == 20:
            self.position[1] += 1
            self.y_moved = 0
        if self.required_direction != self.direction:
            if self.x_moved == 0 and self.y_moved == 0 and can_move(self.required_direction, self.position, base_map):
                self.direction = self.required_direction
                if self.marker == 1:
                    if self.direction == 0:
                        self.image = self.image0
                    elif self.direction == 1:
                        self.image = self.image1
                    elif self.direction == 2:
                        self.image = self.image2
                    elif self.direction == 3:
                        self.image = self.image3
        if pacman_map[self.position[1]][self.position[0]] == '*':
            pacman_map[self.position[1]][self.position[0]] = '.'
            self.dot_is_putted = True
        elif pacman_map[self.position[1]][self.position[0]] == 'E':
            pacman_map[self.position[1]][self.position[0]] = '.'
            self.dot_is_putted = True
            self.is_blue = True
        n = []
        n.append(self.position)
        n.append(self.dot_is_putted)
        n.append(self.is_blue)
        return n

    def change_direction(self, new_direction):
        self.required_direction = new_direction

    def start_pos(self, level):
        if level == 2 or level == 6:
            self.position = [14, 25]
            self.rect.y = 500
        else:
            self.position = [14, 26]
            self.rect.y = 520
        self.rect.x = 280
        self.x_moved = 0
        self.y_moved = 0
        self.direction = 2
        self.required_direction = 2


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    for i in range(len(level_map)):
        level_map[i] = list(level_map[i])
    return level_map


def rules_screen():
    intro_text = ["Правила игры в Пакман крайне просты.",
                  "Игрок стрелками управляет кружочком - пакманом.",
                  "За пакманом тем временем гоняются три призрака, которые могут",
                  "есть пакмана.. Цель - собрать как можно болььше точек, каждая ",
                  "приносит 10 очков. При съедании большой точке пакман на короткое ",
                  "время обретает способность есть призраков. За первого призрака дают ",
                  "200 очков, за каждого следующего - вдвое больше предыдущего. Всего 9 ",
                  "уровней. При прохождении последнего Вы будете отосланы в главное меню,",
                  "как и при смерти и нажатии на ESCAPE. Удачи в игре!"]

    fon = pygame.transform.scale(load_image('Pacman_Image.jpg'), (580, 720))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('serif', 15)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, False, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 40
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    rules_running = True
    while rules_running:
        for rules_event in pygame.event.get():
            if rules_event.type == pygame.KEYDOWN or rules_event.type == pygame.MOUSEBUTTONDOWN:
                return True
            elif rules_event.type == pygame.QUIT:
                return False
        pygame.display.flip()


def settings_screen():
    intro_text = ["Это настройки игры Пакман.",
                  "1. Скорочть пакмана и призраков",
                  "(Измеряется в пикселях в секунду, ",
                  "по умолчанию 3 пикселя в секунду",
                  '',
                  "2       2.5       3       3.5       4       4.5       5",
                  '',
                  '2. Настройка цвета пакмана',
                  '',
                  'Красный       Синий       Желтый       Зеленый']
    global pacman_color
    global FPS
    fon = pygame.transform.scale(load_image('Pacman_Image.jpg'), (580, 720))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('serif', 25)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, False, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    settings_running = True
    while settings_running:
        for settings_event in pygame.event.get():
            if settings_event.type == pygame.MOUSEBUTTONDOWN:
                if settings_event.pos[1] >= 320 and settings_event.pos[1] <= 420:
                    if settings_event.pos[0] >= 30 and settings_event.pos[0] < 80:
                        FPS = 40
                        return True
                    elif settings_event.pos[0] >= 80 and settings_event.pos[0] < 160:
                        FPS = 50
                        return True
                    elif settings_event.pos[0] >= 160 and settings_event.pos[0] < 210:
                        FPS = 60
                        return True
                    elif settings_event.pos[0] >= 210 and settings_event.pos[0] < 290:
                        FPS = 70
                        return True
                    elif settings_event.pos[0] >= 290 and settings_event.pos[0] < 340:
                        FPS = 80
                        return True
                    elif settings_event.pos[0] >= 340 and settings_event.pos[0] < 420:
                        FPS = 90
                        return True
                    elif settings_event.pos[0] >= 420 and settings_event.pos[0] <= 490:
                        FPS = 100
                        return True
                elif settings_event.pos[1] >= 550 and settings_event.pos[1] <= 640:
                    if settings_event.pos[0] >= 30 and settings_event.pos[0] < 160:
                        pacman_color = 'Red_'
                        return True
                    elif settings_event.pos[0] >= 160 and settings_event.pos[0] < 280:
                        pacman_color = 'Blue_'
                        return True
                    elif settings_event.pos[0] >= 280 and settings_event.pos[0] < 410:
                        pacman_color = ''
                        return True
                    elif settings_event.pos[0] >= 410 and settings_event.pos[0] <= 530:
                        pacman_color = 'Green_'
                        return True
            elif settings_event.type == pygame.QUIT:
                return False
        pygame.display.flip()


def start_screen():
    intro_text = ["Играть",
                  "Правила",
                  'Настройки']

    fon = pygame.transform.scale(load_image('Pacman_Image.jpg'), (580, 720))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('serif', 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, False, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 220
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    start_running = True
    while start_running:
        for start_event in pygame.event.get():
            if start_event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif start_event.type == pygame.MOUSEBUTTONDOWN:
                if start_event.pos[0] >= 220 and start_event.pos[0] <= 375:
                    if start_event.pos[1] >= 100 and start_event.pos[1] < 175:
                        return True
                    elif start_event.pos[1] >= 175 and start_event.pos[1] < 250:
                        start_running = rules_screen()
                        screen.blit(fon, (0, 0))
                        text_coord = 50
                        for line in intro_text:
                            string_rendered = font.render(line, False, pygame.Color('white'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 50
                            intro_rect.top = text_coord
                            intro_rect.x = 230
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                        if start_screen == False:
                            return False
                    elif start_event.pos[1] >= 250 and start_event.pos[1] < 325:
                        start_running = settings_screen()
                        screen.blit(fon, (0, 0))
                        text_coord = 50
                        for line in intro_text:
                            string_rendered = font.render(line, False, pygame.Color('white'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 50
                            intro_rect.top = text_coord
                            intro_rect.x = 230
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                        if start_screen == False:
                            return False
        if start_running:
            pygame.display.flip()


def generate_level(level, color, hearts):
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
    font = pygame.font.SysFont('serif', 20)
    score_string_rendered = font.render('Score:    ' + str(score), False, pygame.Color('white'))
    score_rect = score_string_rendered.get_rect()
    score_rect.x = 420
    score_rect.y = 30
    screen.blit(score_string_rendered, score_rect)
    high_score_string_rendered = font.render('High score:    ' + str(high_score), False, pygame.Color('white'))
    high_score_rect = high_score_string_rendered.get_rect()
    high_score_rect.x = 20
    high_score_rect.y = 30
    screen.blit(high_score_string_rendered, high_score_rect)
    if hearts >= 1:
        heart_photo1 = load_image('Heart.jpg')
        heart_rect1 = heart_photo1.get_rect()
        heart_rect1.x = 380
        heart_rect1.y = 670
        screen.blit(heart_photo1, heart_rect1)
    if hearts >= 2:
        heart_photo2 = load_image('Heart.jpg')
        heart_rect2 = heart_photo2.get_rect()
        heart_rect2.x = 440
        heart_rect2.y = 670
        screen.blit(heart_photo2, heart_rect2)
    if hearts >= 3:
        heart_photo3 = load_image('Heart.jpg')
        heart_rect3 = heart_photo3.get_rect()
        heart_rect3.x = 500
        heart_rect3.y = 670
        screen.blit(heart_photo3, heart_rect3)


pygame.init()
running = True
directions = ['left', 'down', 'right', 'up']
clock = pygame.time.Clock()
pacman_direction = 2
pink_direction = 2
blue_direction = 2
brown_direction = 0
pacman_color = ''
red_direction = 0
pacman_positions = [14, 26]
red_position = [13, 14]
pink_position = [14, 14]
blue_position = [11, 17]
brown_position = [15, 17]
screen = pygame.display.set_mode((560, 720))
level_number = 1
dots = 0
mark = 0
FPS = 60
base_map = load_level('level' + str(level_number) + '.txt')
pacman_map = load_level('pacman_level' + str(level_number) + '.txt')
n = start_screen()
lives = 3
ghost_mode = 'scatter'
alternating_mods = [[7, 20, 7, 20, 5, 20, 5, 9999999], [7, 20, 7, 20, 5, 1033, 1, 99999999], [5, 20, 5, 20, 1, 1037, 1, 99999999]]
red_ghost = pygame.sprite.Group()
red_ghost.add(RedGhost(red_position, red_direction))
pink_ghost = pygame.sprite.Group()
pink_ghost.add(PinkGhost(pink_position, pink_direction))
blue_ghost = pygame.sprite.Group()
blue_ghost.add(BlueGhost(blue_position, blue_direction))
brown_ghost = pygame.sprite.Group()
brown_ghost.add(BrownGhost(brown_position, brown_direction))
pacman = pygame.sprite.Group()
pacman.add(PacMan(pacman_color))
clock.tick()
combo = 0
score = 0
blue_in_cage = True
brown_in_cage = True
required_dots = [244, 262, 242, 262, 250, 266, 260, 260, 232]
mode_time_number = 0
mode_time = 0
is_blue_times = [10, 10, 9, 9, 8, 7, 7, 6, 6]
is_blue_time = 0
high_score = 0
required_mode_time = 9999999
colors = ['blue', (0, 255, 255), 'yellow', 'purple', 'red', (50, 50, 150), 'mediumvioletred', 'green', 'blue']
while running and n:
    clock.tick(FPS)
    mark += 1
    if mark >= FPS / 3:
        mark = 0
    screen.fill('black')
    generate_level(pacman_map, colors[level_number - 1], lives)
    red_ghost.draw(screen)
    pink_ghost.draw(screen)
    blue_ghost.draw(screen)
    brown_ghost.draw(screen)
    pacman.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pacman_direction = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                pacman_direction = 3
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pacman_direction = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pacman_direction = 2
            if event.key == pygame.K_ESCAPE:
                level_number = 1
                ghost_mode = 'scatter'
                required_mode_time = 9999999
                combo = 0
                red_ghost = pygame.sprite.Group()
                red_ghost.add(RedGhost(red_position, red_direction))
                pink_ghost = pygame.sprite.Group()
                pink_ghost.add(PinkGhost(pink_position, pink_direction))
                brown_ghost = pygame.sprite.Group()
                brown_ghost.add(BrownGhost(brown_position, brown_direction))
                pacman = pygame.sprite.Group()
                pacman.add(PacMan(pacman_color))
                mode_time = 0
                mode_time_number = 0
                dots = 0
                for i in pacman:
                    i.start_pos(1)
                for i in red_ghost:
                    i.start_pos()
                for i in pink_ghost:
                    i.start_pos()
                for i in blue_ghost:
                    if not blue_in_cage:
                        i.start_pos
                for i in brown_ghost:
                    if not brown_in_cage:
                        i.start_pos()
                lives = 3
                score = 0
                n = start_screen()
            for i in pacman:
                i.change_direction(pacman_direction)
    if mark == 0:
        for i in pacman:
            i.changing()
    if dots >= 80 and blue_in_cage:
        blue_in_cage = False
        for i in blue_ghost:
            i.start_pos()
    if dots >= 120 and brown_in_cage:
        brown_in_cage = False
        for i in brown_ghost:
            i.start_pos()
    for i in pacman:
        temporary_pacman = i.update()
    pacman_position = temporary_pacman[0]
    if temporary_pacman[1]:
        dots += 1
        score += 10
    if temporary_pacman[2]:
        for i in red_ghost:
            red_position = i.change_direction()
        for i in pink_ghost:
            pink_position = i.change_direction()
        for i in blue_ghost:
            blue_position = i.change_direction()
        for i in brown_ghost:
            brown_position = i.change_direction()
        required_mode_time = mode_time
        required_ghost_mode = ghost_mode
        ghost_mode = 'scared'
        mode_time -= is_blue_times[level_number - 1] * 60 - is_blue_time
        is_blue_time = is_blue_times[level_number - 1] * 60
    if required_mode_time == mode_time:
        required_mode_time = 9999999
        combo = 0
        ghost_mode = required_ghost_mode
    if is_blue_time > 0:
        is_blue_time -= 1
    for red_ghost1 in red_ghost:
        red_position = red_ghost1.update(pacman_position, ghost_mode, base_map)
    for pink_ghost1 in pink_ghost:
        pink_position = pink_ghost1.update(pacman_position, ghost_mode, base_map, pacman_direction)
    for blue_ghost1 in blue_ghost:
        blue_position = blue_ghost1.update(pacman_position, ghost_mode, base_map, red_position, pacman_direction)
    for brown_ghost1 in brown_ghost:
        brown_position = brown_ghost1.update(pacman_position, ghost_mode, base_map)
    if dots == required_dots[level_number - 1]:
        level_number += 1
        if level_number <= 9:
            base_map = load_level('level' + str(level_number) + '.txt')
            pacman_map = load_level('pacman_level' + str(level_number) + '.txt')
            lives = 3
            mode_time_number = 0
            mode_time = 0
            ghost_mode = 'scatter'
            required_mode_time = 9999999
            combo = 0
            dots = 0
            brown_in_cage = True
            blue_in_cage = True
            for i in pacman:
                i.start_pos(level_number)
            for i in red_ghost:
                i.start_pos()
            for i in pink_ghost:
                i.start_pos()
            for i in blue_ghost:
                i.position = [15, 16]
                i.rect.x = 300
                i.rect.y = 320
                i.moved = 0
                i.direction = 2
            for i in brown_ghost:
                i.position = [15, 16]
                i.rect.x = 300
                i.rect.y = 320
                i.moved = 0
                i.direction = 2
        else:
            level_number = 1
            ghost_mode = 'scatter'
            required_mode_time = 9999999
            combo = 0
            red_ghost = pygame.sprite.Group()
            red_ghost.add(RedGhost(red_position, red_direction))
            pink_ghost = pygame.sprite.Group()
            pink_ghost.add(PinkGhost(pink_position, pink_direction))
            blue_ghost = pygame.sprite.Group()
            blue_ghost.add(BlueGhost(blue_position, blue_direction))
            brown_ghost = pygame.sprite.Group()
            brown_ghost.add(BrownGhost(brown_position, brown_direction))
            pacman = pygame.sprite.Group()
            pacman.add(PacMan(pacman_color))
            mode_time = 0
            mode_time_number = 0
            dots = 0
            brown_in_cage = True
            blue_in_cage = True
            for i in pacman:
                i.start_pos(1)
            for i in red_ghost:
                i.start_pos()
            for i in pink_ghost:
                i.start_pos()
            lives = 3
            score = 0
            n = start_screen()
    if level_number == 1:
        mode_times = alternating_mods[0]
    elif level_number < 5:
        mode_times = alternating_mods[1]
    else:
        mode_times = alternating_mods[2]
    mode_time += 1
    if mode_time >= mode_times[mode_time_number] * 40:
        mode_time_number += 1
        mode_time = 0
        if mode_time_number % 2 == 0:
            ghost_mode = 'scatter'
        else:
            ghost_mode = 'chase'
        for i in red_ghost:
            red_position = i.change_direction()
        for i in pink_ghost:
            pink_position = i.change_direction()
        for i in blue_ghost:
            blue_position = i.change_direction()
        for i in brown_ghost:
            brown_position = i.change_direction()
    if (pacman_position == red_position or pacman_position == pink_position or pacman_position == brown_position or pacman_position == blue_position) and ghost_mode != 'scared':
        lives -= 1
        ghost_mode = 'scatter'
        for i in pacman:
            i.start_pos(level_number)
        for i in red_ghost:
            i.start_pos()
        for i in pink_ghost:
            i.start_pos()
        for i in blue_ghost:
            if not blue_in_cage:
                i.start_pos()
        for i in brown_ghost:
            if not brown_in_cage:
                i.start_pos()
        mode_time_number = 0
        mode_time = 0
    if pacman_position == brown_position and ghost_mode == 'scared':
        combo += 1
        score += 100 * 2**combo
        for i in brown_ghost:
            i.start_pos()
    if pacman_position == pink_position and ghost_mode == 'scared':
        combo += 1
        score += 100 * 2**combo
        for i in pink_ghost:
            i.start_pos()
    if pacman_position == red_position and ghost_mode == 'scared':
        combo += 1
        score += 100 * 2**combo
        for i in red_ghost:
            i.start_pos()
    if pacman_position == blue_position and ghost_mode == 'scared':
        combo += 1
        score += 100 * 2**combo
        for i in blue_ghost:
            i.start_pos()
    if score > high_score:
        high_score = score
    if lives == 0:
        level_number = 1
        ghost_mode = 'scatter'
        required_mode_time = 9999999
        combo = 0
        red_ghost = pygame.sprite.Group()
        red_ghost.add(RedGhost(red_position, red_direction))
        pink_ghost = pygame.sprite.Group()
        pink_ghost.add(PinkGhost(pink_position, pink_direction))
        blue_ghost = pygame.sprite.Group()
        blue_ghost.add(BlueGhost(blue_position, blue_direction))
        brown_ghost = pygame.sprite.Group()
        brown_ghost.add(BrownGhost(brown_position, brown_direction))
        pacman = pygame.sprite.Group()
        pacman.add(PacMan(pacman_color))
        mode_time = 0
        mode_time_number = 0
        dots = 0
        blue_in_cage = True
        brown_in_cage = True
        for i in pacman:
            i.start_pos(1)
        for i in red_ghost:
            i.start_pos()
        for i in pink_ghost:
            i.start_pos()
        lives = 3
        score = 0
        n = start_screen()
    if n:
        pygame.display.flip()
pygame.quit()