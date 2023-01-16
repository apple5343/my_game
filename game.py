import pygame
import sys
import os
import random
import time
import math
from threading import *
from numba import jit
time_atack = 1
c1 = 1
right = True
left = False
improvement_list = ["Урон увеличивается на 1", "Максимальный ОЗ увеличивается на 1", "Получаемый урон уменьшается на 1",
                    "Молния стреляет в случайного врага", "Здровье + 1", "Увеличивается область поднятия предметов"]
atack_list = []
pygame.init()
kills = 0
pygame.init()
screen_size = (800, 800)
size = (800, 800)

def improvement(screen, zize):
    pygame.draw.rect(screen, (255, 255, 255),
                     (size[0] // 2 - 400, size[1] // 2 - 200, 800, 400))
    btns = pygame.sprite.Group()
    improvement_list_new = random.sample(improvement_list, 3)
    text = []
    for i in range(3):
        Improvement_btn(btns, name=improvement_list_new[i], count=i)
        text.append((size[0] // 2 - 400 + i * 270, size[1] // 2 - 120 + 5))
    btns.draw(screen)
    for i in range(3):
        font = pygame.font.SysFont(None, 20)
        img = font.render(improvement_list_new[i], True, (255, 0, 0))
        screen.blit(img, text[i])
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in btns:
                    if i.rect.collidepoint(event.pos):
                        run = False
                        improvement_add(i.name)
                        break


def pause(screen):
    pass


def improvement_add(name):
    if name == "Урон увеличивается на 1":
        player.damage_k += 1
    elif name == "Максимальный ОЗ увеличивается на 10%":
        player.life_player_max *= 1.1
    elif name == "Получаемый урон уменьшается на 1":
        player.shield += 1
    elif name == "Молния стреляет в случайного врага":
        MYEVENTTYPE_2 = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE_2, 2500)
        atack_2 = pygame.sprite.Group()
        Atack_2(atack_2)
        atack_list.append([MYEVENTTYPE_2, 2, atack_2])
    elif name == "Здровье + 1":
         if player.life_player + 1 <= player.life_player_max:
             player.life_player += 1
    elif name == "Увеличивается область поднятия предметов":
        region.update()

class Improvement_btn(pygame.sprite.Sprite):
    def __init__(self, *group, name, count):
        super().__init__(*group)
        self.image = pygame.Surface((250, 300))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = size[0] // 2 - 400 + count * 270
        self.rect.y = size[1] // 2 - 120
        self.name = name


def move(group, speed, size, player):
    for i in group:
        if pygame.sprite.collide_rect(i, player):
            if i.timer <= 0:
                player.life_player -= i.damage - player.shield
                i.timer = 10
        i.timer -= 0.1
        x = size[0] // 2 - i.rect.x
        y = size[1] // 2 - i.rect.y
        if x > 0:
            i.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)), 360)
            i.rect.x = math.ceil(float(i.rect.x) + speed)
        elif x < 0:
            i.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
                180)
            i.rect.x -= speed
        if y > 0:
            i.rect.y = math.ceil(float(i.rect.y) + speed)
            if not x > 0 and not x < 0:
                i.image = pygame.transform.rotate(
                    pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
                    260)
        elif y < 0:
            if not x > 0 and not x < 0:
                i.image = pygame.transform.rotate(
                    pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
                    90)
            i.rect.y -= speed


class Player(pygame.sprite.Sprite):
    def __init__(self):
        global screen_size
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/mar.png")
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] // 2
        self.rect.y = screen_size[1] // 2
        self.size = self.image.get_size()
        self.shield = 0
        self.life_player_max = 20
        self.damage_k = 0
        self.life_player = 2
        self.coords_x = screen_size[0] // 2
        self.coords_y = screen_size[1] // 2


class Object(pygame.sprite.Sprite):
    def __init__(self, *group):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/tree2.png"), (60, 60))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = random.randrange(- 2000, 2000)
        self.rect.y = random.randrange(- 2000, 2000)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, key, speed):
        global right
        global left
        if key[pygame.K_UP] and any([pygame.sprite.collide_mask(i, player) for i in objects]):
            for i in objects:
                i.rect.y -= speed
        if key[pygame.K_DOWN] and any([pygame.sprite.collide_mask(i, player) for i in objects]):
            for i in objects:
                i.rect.y += speed
        if key[pygame.K_RIGHT] and any([pygame.sprite.collide_mask(i, player) for i in objects]):
            right = True
            left = False
            for i in objects:
                i.rect.x += speed
        if key[pygame.K_LEFT] and any([pygame.sprite.collide_mask(i, player) for i in objects]):
            for i in objects:
                i.rect.x -= speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group, damage, life):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        x = [[size[0], size[0] + 200], [- 200, 0]]
        y = [[size[1], size[1] + 200], [- 200, 0]]
        x2 = random.choice(x)
        y2 = random.choice(y)
        self.rect.x = float(random.randint(x2[0], x2[1]))
        self.rect.y = float(random.randint(y2[0], y2[1]))
        self.timer = 0
        self.life_enemy = life
        self.damage = damage

    def update(self, key, speed):
        if key[pygame.K_UP]:
            self.rect.y += speed
        if key[pygame.K_DOWN]:
            self.rect.y -= speed
        if key[pygame.K_RIGHT]:
            self.rect.x -= speed
        if key[pygame.K_LEFT]:
            self.rect.x += speed


class Atack(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/kk.png"), (80, 20))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = size[0] // 2 + 20
        self.rect.y = size[1] // 2 + 10
        self.damage = 1
        self.kd = 1

    def update(self):
        global atack, experience_1, damage_k
        if right:
            for i in atack:
                i.rect.x = size[0] // 2 + 20
        else:
            for i in atack:
                i.rect.x = size[0] // 2 - 75
        for i in enemy_1:
            for t in atack:
                if pygame.sprite.collide_rect(i, t):
                    i.life_enemy -= t.damage + damage_k
                    if i.life_enemy <= 0:
                        Experience(experience_1, coords=[i.rect.x, i.rect.y])
                        i.kill()
                        global kills
                        kills += 1
                    elif right:
                        i.rect.x += 10
                    else:
                        i.rect.x -= 10


class Atack_2(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/lightning.png"), (300, 600))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.last_atack = 0
        self.kd = 2
        self.rect.x = 0
        self.rect.y = 0
        self.damage = 2

    def update(self):
        c = [i for i in enemy_1 if i.rect.x in range(0, size[0]) and i.rect.y in range(0, size[1])]
        if c:
            enemy = random.choice(c)
            self.rect.x = enemy.rect.x - 135
            self.rect.y = enemy.rect.y - 500
            enemy.life_enemy -= 2 + damage_k
            if enemy.life_enemy <= 0:
                enemy.kill()
        else:
            self.rect.x = 100000000
            self.rect.y = 100000000


class Experience(pygame.sprite.Sprite):
    def __init__(self, *group, coords):
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/experience.png"), (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def update(self, key, speed):
        if key[pygame.K_UP]:
            self.rect.y += speed
        if key[pygame.K_DOWN]:
            self.rect.y -= speed
        if key[pygame.K_RIGHT]:
            self.rect.x -= speed
        if key[pygame.K_LEFT]:
            self.rect.x += speed


class Region(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.region_size = 40
        image = pygame.Surface([self.region_size, self.region_size], pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2
        self.rect.y = size[1] // 2

    def update(self):
        self.region_size += 2
        image = pygame.Surface([self.region_size, self.region_size], pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()


text = pygame.font.Font(None, 36)
kills_record_text = pygame.font.Font(None, 36)
wave_record_text = pygame.font.Font(None, 36)
text = text.render("Играть", True,
                   (200, 0, 0))


def start_screen():
    global text, kills_record_text, wave_record_text
    start_screen = pygame.display.set_mode((800, 800))
    running = True
    fps = 60
    clock = pygame.time.Clock()
    start_btn = pygame.sprite.Group()
    Start_btn(start_btn)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in start_btn:
                    if i.rect.collidepoint(event.pos):
                        return True
        start_screen.fill((173, 255, 47))
        start_btn.draw(start_screen)
        start_screen.blit(text, (350, 320))
        start_screen.blit(wave_record_text, (300, 500))
        start_screen.blit(kills_record_text, (450, 500))
        clock.tick(fps)
        pygame.display.flip()


def k():
    move_t = Thread(target=move, args=(enemy_1, 0.1, size, player))
    move_t.start()


class Start_btn(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((150, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 300

if __name__ == '__main__':
    f1 = pygame.font.Font(None, 36)
    with open("record.txt") as f:
        a = f.read()
        kills_record = a.split("\n")[0]
        wave_record = a.split("\n")[1]
        kills_record_text = kills_record_text.render("Убийства: " + kills_record, True,
                                                    (200, 0, 0))
        wave_record_text = wave_record_text.render("Волны :" + wave_record, True,
                                                    (200, 0, 0))
    if start_screen():
        pygame.init()
        pygame.display.set_caption('Игра')
        #screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        screen = pygame.display.set_mode((800, 800))
        size = screen.get_size()
        screen_size = screen.get_size()
        all_sprites = pygame.sprite.Group()
        objects = pygame.sprite.Group()
        enemy_1 = pygame.sprite.Group()
        atack = pygame.sprite.Group()
        experience_1 = pygame.sprite.Group()
        region = pygame.sprite.Group()
        player = Player()
        damage_k = 0
        all_sprites.add(player)
        screen.fill((0, 0, 255))
        Atack(atack)
        region_1 = Region()
        region.add(region_1)
        experience_status = 0
        experience_status_max = 30
        count_enemy = 3
        damage_enemy = 1
        life_enemy = 1
        for _ in range(15):
            Object(objects)
        for i in range(random.randint(2, 3)):
            Enemy(enemy_1, damage=damage_enemy, life=life_enemy)
        running = True
        fps = 60
        wave = 1
        speed = 2
        clock = pygame.time.Clock()
        MYEVENTTYPE_1 = pygame.USEREVENT + 0
        pygame.time.set_timer(MYEVENTTYPE_1, 1000)
        atack_list.append([MYEVENTTYPE_1, 1, atack])
        kills = 0
        while running:
            if player.life_player <= 0:
                running = False
                with open("record.txt") as f:
                    a = f.read()
                    kills_record = a.split("\n")[0]
                    wave_record = a.split("\n")[1]
                if wave > int(wave_record) or kills > int(kills_record):
                    with open("record.txt", mode="w") as f:
                        if wave > int(wave_record):
                            wave_record = wave
                        if kills > int(kills_record):
                            kills_record = kills
                        f.write(f"{kills_record}\n{wave_record}")
                wait = True
                game_over = pygame.font.Font(None, 36)
                game_over = game_over.render('Игра окончена', True,
                                  (180, 0, 0))
                screen.blit(game_over, (310, 100))
                wave_results = pygame.font.Font(None, 36)
                wave_results = wave_results.render('Волны: ' + str(wave), True,
                                  (180, 0, 0))
                screen.blit(wave_results, (200, 300))
                kills_results = pygame.font.Font(None, 36)
                kills_results = kills_results.render('Убийства: ' + str(kills), True,
                                  (180, 0, 0))
                screen.blit(kills_results, (400, 300))
                pygame.display.flip()
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            wait = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for i in atack_list:
                    if event.type == i[0]:
                        i[2].update()
                        i[2].draw(screen)
                        pygame.display.flip()
            keys = pygame.key.get_pressed()
            if len(enemy_1) == 0:
                wave += 1
                if wave % 2 == 0:
                    life_enemy += 1
                    for i in range(count_enemy):
                        Enemy(enemy_1, damage=damage_enemy, life=life_enemy)
                else:
                    count_enemy += 1
                    damage_enemy += 1
                    for i in range(wave):
                        Enemy(enemy_1, damage=damage_enemy, life=life_enemy)
                move_t = Thread(target=move, args=(enemy_1, 0.1, size, player))

            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                if keys[pygame.K_UP] and player.coords_y + 1 <= 1000:
                    player.coords_y += 1
                    for i in objects:
                        i.rect.y += speed
                if keys[pygame.K_DOWN] and player.coords_y - 1 >= - 1000:
                    player.coords_y -= 1
                    for i in objects:
                        i.rect.y -= speed
                if keys[pygame.K_LEFT] and player.coords_x - 1 >= - 1000:
                    player.coords_x -= 1
                    right = False
                    left = True
                    for i in objects:
                        i.rect.x += speed
                if keys[pygame.K_RIGHT] and player.coords_x + 1 <= 1000:
                    player.coords_x += 1
                    right = True
                    left = False
                    for i in objects:
                        i.rect.x -= speed
                c = [pygame.sprite.collide_rect(i, player) for i in objects]
                if not any(c) and - 999 < player.coords_x < 999 and - 999 < player.coords_y < 999:
                    enemy_1.update(keys, speed)
                    experience_1.update(keys, speed)
                objects.update(keys, speed)
            screen.fill((173, 255, 47))
            objects.draw(screen)
            all_sprites.draw(screen)
            enemy_1.draw(screen)
            text1 = f1.render('Жизни: ' + str(player.life_player), True, (100, 0, 0))
            screen.blit(text1, (30, 30))
            for i in experience_1:
                if pygame.sprite.collide_rect(i, region_1):
                    experience_status += 30
                    if experience_status >= experience_status_max:
                        experience_status_max = round(experience_status * 1.2)
                        experience_status = 0
                        improvement(screen, screen_size)
                    i.kill()
            k()
            experience_1.draw(screen)
            region.draw(screen)
            pygame.draw.rect(screen, (0, 0, 0), (screen_size[0] - 600, 20, 500, 60), 2)
            pygame.draw.rect(screen, (255, 255, 255), (screen_size[0] - 598, 19, 5 * (100 * experience_status) // experience_status_max - 1, 59))
            clock.tick(fps)
            pygame.display.flip()
        pygame.display.quit()

