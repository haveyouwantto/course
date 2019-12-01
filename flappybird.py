# -*- coding:utf-8 -*-
import sys
import random

import pygame

width, height = 640, 480

# 调试
debug = False

# 全屏
fullscreen = False


# # 资源文件路径类
class res:
    resources = 'resources/'
    images = resources + 'images/'
    bg = pygame.image.load(images + 'bg_day.png')
    bird = (
        pygame.image.load(images + '0.png'), pygame.image.load(images + '1.png'), pygame.image.load(images + '2.png'))
    over = pygame.image.load(images + 'over.png')


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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 3
        if keys[pygame.K_RIGHT]:
            self.x += 3
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


# 方块类
class Rectangle:
    def __init__(self, surface, color, gappos, gapsize, x):
        self.surface = surface
        self.color = color
        self.x1 = width - x
        self.y1 = 0
        self.width = 50
        self.height1 = gappos
        self.height2 = height
        self.x2 = width
        self.y2 = gappos + gapsize

    def update(self):
        pygame.draw.rect(self.surface, self.color, (self.x1, self.y1, self.width, self.height1))
        pygame.draw.rect(self.surface, self.color, (self.x2, self.y2, self.width, self.height2))
        self.x1 -= 2.5
        self.x2 = self.x1
        '''
        if (debug):
            self.surface.blit(txt_img('simhei', 18, "{0} {1}".format(self.y1 + self.height1, self.x1), (255, 255, 255)),
                              (self.x1 + 5, self.y1 + self.height1 - 20))
            self.surface.blit(txt_img('simhei', 18, "{0}".format(self.y2), (255, 255, 255)),
                              (self.x1 + 5, self.y2))
        '''

        if (self.x1 < -self.width):
            return True

    def get_gap_y(self):
        return (self.y1 + self.height1, self.y2)

    def get_x(self):
        return (self.x1, self.x1 + self.width)


def txt_img(font, size, text, color):
    f = pygame.font.SysFont(font, size)
    return f.render(text, True, color)


# # 初始化界面
pygame.init()
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('flappy bird')
pygame.display.set_icon(res.bird[0])

clock = pygame.time.Clock()

# 背景
bg = res.bg
bg2 = pygame.transform.scale(bg, (width, height))
screen.blit(bg2, (0, 0))

# 更新屏幕
pygame.display.update()

while True:
    rects = []
    score = 0
    game_over = False
    retry = False

    # 小鸟
    bird = Bird()
    screen.blit(bird.image, (bird.x, bird.y))

    # 获取开始时刻
    start = pygame.time.get_ticks()
    actual = 0

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
                            (width, height), pygame.FULLSCREEN | pygame.HWSURFACE)
                    else:
                        screen = pygame.display.set_mode((width, height))
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        if actual % 80 == 0 and actual > 60:
            rects.append(Rectangle(screen, (50, 75, 35), random.randint(50, width - 300), 150, 0))

        screen.blit(bg2, (0, 0))
        bird.update()
        screen.blit(bird.image, (bird.x, bird.y))
        for i in rects:
            passed = i.update()
            if passed:
                rects.remove(i)
                score += 1
            gap_y = i.get_gap_y()
            i_x = i.get_x()
            if bird.x > i_x[0] - 30 and bird.x < i_x[1] and (bird.y < gap_y[0] - 10 or bird.y > gap_y[1] - 40):
                game_over = True

        if bird.x > width:
            game_over = True

        if game_over:
            break

        info = txt_img('simhei', 18, '[空格] 弹跳  [方向键左右] 左右移动  [F3] 调试信息  [F11] 全屏', (255, 255, 255))
        screen.blit(info, (0, 0))

        scoretxt = txt_img(None, 48, str(score), (255, 255, 255))
        screen.blit(scoretxt, (10, 30))

        current = pygame.time.get_ticks()

        # 帧率计算
        theory = (current - start) / 50 * 3
        actual += 1
        drop = theory / actual * 100 - 100

        if (debug):
            screen.blit(txt_img('simhei', 18,
                                "X: {:.2f}  Y: {:.2f}  S: {:.2f}".format(bird.x, bird.y,
                                                                         bird.ys), (52, 127, 66)),
                        (0, height - 40))
            screen.blit(txt_img('simhei', 18, "处理落率: {:.2f}% ({:.2f} fps)".format(drop, clock.get_fps()), (52, 127, 66)),
                        (0, height - 20))

        pygame.display.update()

        clock.tick(60)

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
                            (width, height), pygame.FULLSCREEN | pygame.HWSURFACE)
                    else:
                        screen = pygame.display.set_mode((width, height))
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    retry = True

        if retry:
            break

        screen.blit(bg2, (0, 0))
        screen.blit(res.over, (width / 2 - 100, height / 2 - 100))
        screen.blit(txt_img('simhei', 36, "你的得分: {0}".format(score), (255, 255, 255)),
                    (width / 2 - 100, height / 2 - 40))
        screen.blit(txt_img('simhei', 24, "处理落率: {:.2f}%".format(drop), (255, 255, 255)),
                    (width / 2 - 100, height / 2))
        screen.blit(txt_img('simhei', 24, "[F11] 全屏 [ESC] 退出 [R] 重玩", (255, 255, 255)),
                    (0, 0))
        pygame.display.update()

        clock.tick(60)
