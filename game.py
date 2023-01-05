import pygame
import sys
import os
import random
import time
import math
from threading import *
time_atack = 1
c1 = 1
right = True
left = False
improvement_list = ["Урон увеличивается на 1", "Максимальный ОЗ увеличивается на 10%", "Получаемый урон уменьшается на 1"]


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


def improvement_add(name):
    global damage_k
    global life_player_max
    global shield
    if name == "Урон увеличивается на 1":
        print(damage_k)
        damage_k += 1
        print(damage_k)
    elif name == "Максимальный ОЗ увеличивается на 10%":
        print(life_player_max)
        life_player_max *= 1.1
        print(life_player_max)
    elif name == "Получаемый урон уменьшается на 1":
        print(shield)
        shield += 1
        print(shield)


class Improvement_btn(pygame.sprite.Sprite):
    def __init__(self, *group, name, count):
        super().__init__(*group)
        self.image = pygame.Surface((250, 300))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = size[0] // 2 - 400 + count * 270
        self.rect.y = size[1] // 2 - 120
        self.name = name



def timer(screen):
    global time_atack
    while True:
        time.sleep(0.01)
        time_atack += 0.01


def move(group, speed, size):
    global shield
    global life_player
    for i in group:
        if pygame.sprite.collide_rect(i, player):
            if i.timer <= 0:
                life_player -= i.damage - shield
                i.timer = 10
        i.timer -= 0.1
        x = size[0] // 2 - i.rect.x
        y = size[1] // 2 - i.rect.y
        if x > 0:
            i.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)), 360)
            i.rect.x = math.ceil(float(i.rect.x) + speed)
        elif x < 0:
            i.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
                                              180)
            i.rect.x -= speed
        if y > 0:
            i.rect.y = math.ceil(float(i.rect.y) + speed)
            i.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
                                              260)
        elif y < 0:
            i.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60)),
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


class Object(pygame.sprite.Sprite):
    def __init__(self, *group):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/tree2.png"), (60, 60))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = random.randrange(1000)
        self.rect.y = random.randrange(1000)
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
    def __init__(self, *group):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load("data/zombie2.png"), (60, 60))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = float(random.randrange(1000))
        self.rect.y = float(random.randrange(1000))
        self.timer = 0
        self.life_enemy = 2
        self.damage = 4

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
        self.image = pygame.Surface((50, 20))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = size[0] // 2 + 20
        self.rect.y = size[1] // 2 + 10
        self.damage = 1

    def update(self):
        if right:
            for i in atack:
                i.rect.x = size[0] // 2 + 20
        else:
            for i in atack:
                i.rect.x = size[0] // 2 - 50
        for i in enemy_1:
            for t in atack:
                if pygame.sprite.collide_rect(i, t):
                    i.life_enemy -= t.damage + damage_k
                    if i.life_enemy <= 0:
                        Experience(experience_1, coords=[i.rect.x, i.rect.y])
                        i.kill()
                    elif right:
                        i.rect.x += 10
                    else:
                        i.rect.x -= 10


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
        image = pygame.Surface([40, 40], pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2
        self.rect.y = size[1] // 2

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра')
    #screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    screen = pygame.display.set_mode((1000, 1000))
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
    shield = 0
    for _ in range(8):
        Object(objects)
    for _ in range(10):
        Enemy(enemy_1)
    t1 = Thread(target=timer, args=(screen, ))
    t1.start()
    running = True
    y = 20
    v = 10
    fps = 60
    speed = 2
    clock = pygame.time.Clock()
    f1 = pygame.font.Font(None, 36)
    life_player = 20
    life_player_max = 20
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_UP]:
                for i in objects:
                    i.rect.y += speed
            if keys[pygame.K_DOWN]:
                for i in objects:
                    i.rect.y -= speed
            if keys[pygame.K_LEFT]:
                right = False
                left = True
                for i in objects:
                    i.rect.x += speed
            if keys[pygame.K_RIGHT]:
                right = True
                left = False
                for i in objects:
                    i.rect.x -= speed
            c = [pygame.sprite.collide_rect(i, player) for i in objects]
            if not any(c):
                enemy_1.update(keys, speed)
                experience_1.update(keys, speed)
            objects.update(keys, speed)
        move(enemy_1, 10 / fps, size)
        screen.fill((0, 0, 255))
        objects.draw(screen)
        all_sprites.draw(screen)
        enemy_1.draw(screen)
        text1 = f1.render('Жизни: ' + str(life_player), True,
                          (100, 0, 0))
        screen.blit(text1, (10, 10))
        if time_atack > 2:
            atack.update()
            time_atack = 0
            atack.draw(screen)
        for i in experience_1:
            if pygame.sprite.collide_rect(i, region_1):
                experience_status += 30
                if experience_status >= experience_status_max:
                    experience_status_max = round(experience_status * 1.2)
                    experience_status = 0
                    improvement(screen, screen_size)
                i.kill()
        experience_1.draw(screen)
        region.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), (screen_size[0] - 600, 20, 500, 60), 2)
        pygame.draw.rect(screen, (255, 255, 255), (screen_size[0] - 598, 19, 5 * (100 * experience_status) // experience_status_max - 1, 59))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()