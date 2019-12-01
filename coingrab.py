# -*- coding:utf-8 -*-

from sys import exit

import pygame
from pygame import *

import random


class Player:
    def __init__(self, x, y):
        self.image = [pygame.image.load('resources/images/left.png'), pygame.image.load('resources/images/right.png')]
        self.x = x
        self.y = y
        self.facing = 1

    def update(self, screen):
        mousepos = pygame.mouse.get_pos()
        self.x = mousepos[0]
        self.draw(screen)

    def getFacing(self):
        rel = pygame.mouse.get_rel()[0]
        if rel > 0:
            return 1
        elif rel < 0:
            return 0
        else:
            return self.facing

    def draw(self, screen):
        self.facing = self.getFacing()
        screen.blit(self.image[self.facing], (self.x, self.y))


class Game:
    RUN = 0
    PAUSE = 1

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.bg = pygame.image.load('resources/images/background.png')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.state = Game.RUN

        pygame.display.set_caption("Coin Grab")

        # 玩家
        self.player = Player(0, self.height * 0.62)

    # 主循环
    def run(self):
        while self.state == Game.RUN:
            self.listen()
            self.control()

    # 事件监听
    def listen(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    # 控制游戏
    def control(self):
        self.screen.blit(self.bg, (0, 0))
        self.player.update(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    g = Game()
    g.run()
