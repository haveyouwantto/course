# -*- coding:utf-8 -*-
import sys

import pygame

import random


class Ball:
    def __init__(self, x, y, xs, ys, color, name="Ball"):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.color = color
        self.score = 0
        self.bhcolor = 0
        self.detect = True
        self.name = name

    def update(self, screen):
        if self.detect and self.score >= 5:
            self.bhcolor = 255
            self.detect = False
        self.x += self.xs
        self.y += self.ys
        self.shape = pygame.draw.circle(
            screen, self.color, (self.x, self.y), 20)
        self.bounce()

    def x_bounce(self):
        self.xs = -self.xs

    def y_bounce(self):
        self.ys = -self.ys

    def bounce(self):
        if self.x > 620 or self.x < 20:
            self.x_bounce()

        if self.y > 460 or self.y < 20:
            self.y_bounce()

        if self.x < 19:
            self.x = 21
        if self.x > 621:
            self.x = 619
        if self.y < 19:
            self.y = 21
        if self.y > 461:
            self.y = 459

    def move(self, x, y):
        self.x = x
        self.y = y


def txt_img(font, size, text, color):
    f = pygame.font.SysFont(font, size)
    return f.render(text, True, color)


def intro(screen):
    s = txt_img('simhei', 24, '当移动的小球靠近黑洞时...', (255, 0, 0))
    screen.blit(s, (100, 200))
    pygame.display.update()
    pygame.time.delay(2000)
    screen.fill((0, 0, 0))
    s = txt_img('simhei', 24, '迅速按下鼠标左键以收集能量！', (255, 0, 0))
    screen.blit(s, (100, 200))
    pygame.display.update()
    pygame.time.delay(2000)
    screen.fill((0, 0, 0))


pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('拯救黑洞')

intro(screen)

r = Ball(20, 20, 4, 4, (255, 0, 0), "红球")
g = Ball(124, 352, 4, 4, (0, 255, 0), "绿球")
l = [r, g]

blackhole = pygame.draw.circle(screen, (0, 0, 0), (320, 240), 75)

clock = pygame.time.Clock()

start = pygame.time.get_ticks()

fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            try:
                if event.button == 1:
                    for i in l:
                        if blackhole.contains(i.shape) and i.detect:
                            i.score += 1
                            i.bhcolor += 51
                            pygame.time.delay(200)
                            i.move(random.randint(30, 600),
                                   random.randint(30, 320))
                            i.xs = random.randint(3, 9)
                            i.ys = random.randint(3, 9)
                if event.button == 3:
                    for i in l:
                        i.xs = random.randint(3, 9)
                        i.ys = random.randint(3, 9)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(
                        (640, 480), pygame.FULLSCREEN | pygame.HWSURFACE)
                else:
                    screen = pygame.display.set_mode((640, 480))
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_ESCAPE:
                exit()

    screen.fill([255, 255, 255])
    t2 = pygame.time.get_ticks()

    if r.score >= 5 and g.score >= 5:
        pygame.draw.circle(screen, (255, 255, 0), (320, 240), 75)
        s = txt_img(None, 45, 'You Win!', (0, 0, 0))
        screen.blit(s, (260, 225))
        pygame.display.update()
        continue

    if t2 - start >= 60000:
        pygame.draw.circle(screen, (0, 0, 0), (320, 240), 75)
        s = txt_img(None, 45, 'You Lose', (255, 0, 0))
        screen.blit(s, (260, 225))
        pygame.display.update()
        continue

    # 对每个球进行检测
    for i in range(len(l)):
        l[i].update(screen)
        s = txt_img('simhei', 24, l[i].name + '得分: ' + str(l[i].score), (0, 0, 0))
        screen.blit(s, (0, i * 75 + 25))

        xs = txt_img('simhei', 24, l[i].name + '的X速度: ' + str(l[i].xs), (0, 0, 0))
        screen.blit(xs, (0, i * 75 + 50))

        ys = txt_img('simhei', 24, l[i].name + '的Y速度: ' + str(l[i].ys), (0, 0, 0))
        screen.blit(ys, (0, i * 75 + 75))

    blackhole = pygame.draw.circle(screen, (r.bhcolor, g.bhcolor, 0), (320, 240), 75)

    t = txt_img('simhei', 24, '倒计时: ' + str((60000 - (t2 - start)) / 1000), (0, 0, 0))

    screen.blit(t, (0, 0))

    info = txt_img('simhei', 24, '右键 - 改变速度    ESC - 退出游戏    F11 - 全屏', (0, 0, 0))

    screen.blit(info, (0, 450))

    clock.tick(60)

    pygame.display.update()
