# -*- coding:utf-8 -*-
import sys
import random

import pygame

width, height = 640, 480


# # 资源文件路径类
class res:
    resources = 'resources/'
    images = resources + 'images/'
    bg = pygame.image.load(images + 'bg_day.png')
    bird = (
    pygame.image.load(images + '0.png'), pygame.image.load(images + '1.png'), pygame.image.load(images + '2.png'))


# # 小鸟 类
class Bird():
    def __init__(self):
        self.image = res.bird[0]
        self.x = 0
        self.y = 240
        self.xs = 0
        self.ys = 0
        self.lifetime = 0

    def update(self):
        self.ys += 0.25
        self.lifetime += 1
        self.image = res.bird[(self.lifetime % 12) // 4]
        if (self.ys > 10):
            self.ys = 10
        if (self.x < 0):
            self.x = 0
        if (self.y > height - 50):
            self.y = height - 50
        self.y += self.ys


def txt_img(font, size, text, color):
    f = pygame.font.SysFont(font, size)
    return f.render(text, True, color)


# # 初始化界面
pygame.init()
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('flappy bird')

clock = pygame.time.Clock()

# 背景
bg = res.bg
bg2 = pygame.transform.scale(bg, (width, height))
screen.blit(bg2, (0, 0))

# 小鸟
bird = Bird()
screen.blit(bird.image, (bird.x, bird.y))

# 更新屏幕
pygame.display.update()

# # 全局变量设置
# 获取开始时刻
start = pygame.time.get_ticks()
actual = 0

# 调试
debug = False

# 全屏
fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.ys = -5
            elif event.key == pygame.K_F3:
                debug = not debug
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(
                        (640, 480), pygame.FULLSCREEN | pygame.HWSURFACE)
                else:
                    screen = pygame.display.set_mode((640, 480))
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bird.x -= 3
    if keys[pygame.K_RIGHT]:
        bird.x += 3

    screen.blit(bg2, (0, 0))
    bird.update()
    screen.blit(bird.image, (bird.x, bird.y))

    info = txt_img('simhei', 18, '[空格] 弹跳  [方向键左右] 左右移动  [F3] 调试信息  [F11] 全屏', (255, 255, 255))
    screen.blit(info, (0, 0))

    current = pygame.time.get_ticks()

    theory = int((current - start) / 50 * 3) + 1
    actual += 1

    if (debug):
        screen.blit(txt_img('simhei', 18,
                            "X: {0:.2f}  Y: {1:.2f}  X速度: {2:.2f}  Y速度:{3:.2f}".format(bird.x, bird.y, bird.xs,
                                                                                       bird.ys), (255, 255, 255)),
                    (0, 20))
        screen.blit(txt_img('simhei', 18, "处理落率: {:.2f}%".format(theory / actual * 100 - 100), (255, 255, 255)),
                    (0, 40))

    pygame.display.update()

    clock.tick(60)
