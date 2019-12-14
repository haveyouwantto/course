# -*- coding:utf-8 -*-

from sys import exit

import pygame
from pygame import *

import random


class Drop:
    def __init__(self, image, sound, speed, screen):
        self.image = image
        self.sound = sound
        self.rect = self.image.get_rect()
        self.bx = screen.get_rect().right
        self.by = screen.get_rect().bottom
        self.rect.bottom = 0
        self.rect.centerx = random.randint(20, self.bx)
        self.speed = speed

    def update(self, drop_list, screen, player, max_score):
        self.rect.bottom += self.speed
        self.draw(screen)
        self.collide(drop_list, screen, player, max_score)
        if self.rect.top > screen.get_rect().height:
            drop_list.remove(self)

    def collide(self, drop_list, screen, player, max_score):
        if player.rect.colliderect(self.rect):
            self.on_collide(drop_list, screen, player, max_score)

    def on_collide(self, drop_list, screen, player, max_score):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Coin(Drop):
    def __init__(self, speed, screen):
        Drop.__init__(self, pygame.image.load('resources/images/gold1.png'),
                      pygame.mixer.Sound('resources/sounds/bullet.ogg'), speed, screen)

    def on_collide(self, drop_list, screen, player, max_score):
        self.sound.play()
        drop_list.remove(self)
        score = int((player.rect.bottom - self.rect.top) / 145 * max_score)
        player.score += score
        screen.blit(
            txt_img('simhei', 24, "+ {0}".format(score), (255, 0, 0)), self.rect)


class Bomb(Drop):
    def __init__(self, speed, screen):
        Drop.__init__(self, pygame.image.load('resources/images/bomb.png'),
                      pygame.mixer.Sound('resources/sounds/enemy.ogg'), speed, screen)

    def on_collide(self, drop_list, screen, player, max_score):
        self.sound.play()
        drop_list.remove(self)
        player.lives -= 1
        screen.blit(txt_img('simhei', 48, "BOOM!", (255, 0, 0)), self.rect)


# TODO text message
class TextMessage:
    def __init__(self, text, rect):
        self.rect = rect
        self.text = text
        self.time = 0

    def update(self, screen, l):
        screen.blit(txt_img('simhei', 24, self.text, (255, 0, 0)), self.rect)
        self.rect.top -= 1
        self.time += 1
        if self.time > 60:
            l.remove(self)


class DropList:
    COIN = 0
    BOMB = 1

    def __init__(self):
        self.list = []

    def update(self, screen, player, max_score):
        for i in self.list:
            i.update(self, screen, player, max_score)

    def add(self, type, speed, screen):
        if type == 0:
            d = Coin(speed, screen)
        else:
            d = Bomb(speed, screen)
        self.list.append(d)

    def remove(self, drop):
        self.list.remove(drop)


class Player:
    def __init__(self, x, y):
        self.image = [pygame.image.load(
            'resources/images/left.png'), pygame.image.load('resources/images/right.png')]
        self.rect = self.image[0].get_rect()
        self.rect.left = x
        self.rect.top = y
        self.facing = 1
        self.score = 0
        self.lives = 4

    def update(self, screen):
        mousepos = pygame.mouse.get_pos()
        self.rect.centerx = mousepos[0]
        self.draw(screen)

    def get_facing(self):
        rel = pygame.mouse.get_rel()[0]
        if rel > 0:
            return 1
        elif rel < 0:
            return 0
        else:
            return self.facing

    def draw(self, screen):
        self.facing = self.get_facing()
        screen.blit(self.image[self.facing], self.rect)


def txt_img(font, size, text, color):
    f = pygame.font.SysFont(font, size)
    return f.render(text, True, color)


class Game:
    RUN = 0
    PAUSE = 1
    FAIL = 2

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.bg = pygame.image.load('resources/images/background.png')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.state = Game.RUN

        # 设置标题
        pygame.display.set_caption("Coin Grab")

        #pygame.mixer.music.load('resources/sounds/background.ogg')
        #pygame.mixer.music.play()

        # 玩家
        self.player = Player(0, self.height * 0.62)  # 62 %

        self.cl = DropList()

        self.time = 0
        self.clock = pygame.time.Clock()

        # 游戏属性
        self.speed = 4
        self.max_score = 30

        self.pause_sound=pygame.mixer.Sound('resources/sounds/score.ogg')
        self.resume_sound=pygame.mixer.Sound('resources/sounds/bird_die.ogg')

    # 主循环
    def run(self):
        while True:
            self.listen()
            if self.state == Game.RUN:
                self.control()
            elif self.state == Game.FAIL:
                self.fail()
            elif self.state ==Game.PAUSE:
                self.pause()

    # 事件监听
    def listen(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if self.state == Game.FAIL and event.key == K_r:
                    self.reset()
                if event.key == K_ESCAPE:
                    if self.state==Game.RUN:
                        self.pause_sound.play()
                        self.state=Game.PAUSE
                    elif self.state==Game.PAUSE:
                        self.resume_sound.play()
                        self.state=Game.RUN

    # 控制游戏
    def control(self):
        self.time += 1
        self.screen.blit(self.bg, (0, 0))
        self.player.update(self.screen)

        if self.player.lives < 0:
            self.state = Game.FAIL

        if self.time % 31 == 0:
            self.cl.add(DropList.COIN, self.speed, self.screen)
            self.speed += 0.05
            self.max_score = (self.speed / 2 - 1) * 30

        if self.time % 41 == 0:
            self.cl.add(DropList.BOMB, self.speed, self.screen)
            self.max_score = (self.speed / 2 - 1) * 30

        self.cl.update(self.screen, self.player, self.max_score)

        self.draw_text()

        pygame.display.update()
        self.clock.tick(60)

    def fail(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(txt_img('simhei', 48, "游戏结束", (0, 0, 0)),
                         (self.width / 2, self.height / 2))
        self.screen.blit(txt_img('simhei', 24, "得分: {0}".format(self.player.score), (0, 0, 0)),
                         (self.width / 2, self.height / 2 + 48))
        pygame.display.update()
        self.clock.tick(60)

    def pause(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(txt_img('simhei', 48, "游戏暂停", (0, 0, 0)),
                         (self.width / 2, self.height / 2))
        pygame.display.update()
        self.clock.tick(60)

    def draw_text(self):
        self.screen.blit(txt_img('simhei', 24, "得分: {0}".format(
            self.player.score), (0, 0, 0)), (0, 0))
        self.screen.blit(
            txt_img('simhei', 24, "速度: {0:.2f}".format(self.speed), (0, 0, 0)), (0, 30))
        self.screen.blit(txt_img('simhei', 24, "最大得点: {0:.0f}".format(
            self.max_score), (0, 0, 0)), (0, 60))
        self.screen.blit(txt_img('simhei', 24, "剩余生命: {0}".format(
            self.player.lives), (0, 0, 0)), (0, 90))

    def reset(self):
        self.state = Game.RUN
        # 玩家
        self.player = Player(0, self.height * 0.62)  # 62 %

        self.cl = DropList()

        self.time = 0
        self.clock = pygame.time.Clock()

        # 游戏属性
        self.speed = 4
        self.max_score = 30


if __name__ == '__main__':
    g = Game()
    g.run()
