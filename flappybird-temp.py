import pygame
from pygame.locals import *
from sys import exit
from random import randint

# 初始化 pygame
pygame.init()

# 设置窗体
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('这儿是游戏名字')

# 设置背景图片
# 1. 加载图片
bg = pygame.image.load('resources/images/bg_day.png')
bg_new = pygame.transform.smoothscale(bg, (800, 600))
# 2. 贴图
screen.blit(bg_new, (0, 0))
# 3. 更新屏幕
pygame.display.update()

# 设置小鸟图片
# 1. 加载图片
bird = pygame.image.load('resources/images/0.png')
# 2. 贴图
screen.blit(bird, (0, 100))
# 3. 更新屏幕
pygame.display.update()

y = 0

rect_x = 740


class rectangle:
    def __init__(self, surface, color, gappos, gapsize):
        self.surface = surface
        self.color=color
        self.x = 800
        self.y = 0
        self.width = 50
        self.height = gappos

    def update(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height),1)
        self.x -= 2
        print(self.x, self.y, self.width, self.height)


# 让程序侦测到按键持续按下
pygame.key.set_repeat(1, 1)

rects = []
for i in range(100, 300, 200):
    rect = rectangle(screen, (randint(0, 255), randint(0, 255), randint(0, 255)),i,40)
    rects.append(rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                y = y - 10

    screen.blit(bg_new, (0, 0))
    screen.blit(bird, (0, y))
    y = y + 3

    for i in rects:
        i.update()
    pygame.display.update()
