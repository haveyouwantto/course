import sys
import tkinter as tk
import pygame


def txt_img(font, size, text, color):
    f = pygame.font.SysFont(font, size)
    return f.render(text, True, color)


class Player(pygame.sprite.Sprite):
    def __init__(self, parent_surface, size_multiplier):
        pygame.sprite.Sprite.__init__(self)

        # 几何信息
        self.size_multiplier = size_multiplier
        self.image1 = pygame.transform.scale(pygame.image.load('resources/images/myplane1.png'),
                                             (int(64 * size_multiplier), int(80 * size_multiplier)))
        self.image2 = pygame.transform.scale(pygame.image.load('resources/images/myplane2.png'),
                                             (int(64 * size_multiplier), int(80 * size_multiplier)))
        self.parent_surface = parent_surface
        self.bounds = parent_surface.get_size()  # width, height

        self.rect = self.image1.get_rect()
        self.rect.centerx = self.bounds[0] / 2
        self.rect.centery = self.bounds[1] - self.image1.get_height()

        # 声音信息

        self.shoot_sound = pygame.mixer.Sound('resources/sounds/bullet.ogg')

        # 机体属性
        self.speed = 5 * size_multiplier
        self.slow_mode = False
        self.lives = 2
        self.bombs = 3
        self.bomb_cooldown = 0

        self.score = 0
        self.hiscore = 0
        self.power = 0
        self.maxpoint = 10000
        self.graze = 0

        self.lifetime = 0

    def listen(self, bullets):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.move_up()
        if keys[pygame.K_DOWN]:
            self.move_down()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_z]:
            self.shoot(bullets)
        if keys[pygame.K_x] and self.bomb_cooldown == 0:
            self.bomb_cooldown = 240
            self.bomb()
        if keys[pygame.K_LSHIFT]:
            self.slow_mode = True
        elif not keys[pygame.K_LSHIFT]:
            self.slow_mode = False

    def move_up(self):
        if self.rect.centery > 0:
            self.rect.centery -= self.speed
        else:
            self.rect.centery = 0

    def move_down(self):
        if self.rect.centery < self.bounds[1]:
            self.rect.centery += self.speed
        else:
            self.rect.centery = self.bounds[1]

    def move_left(self):
        if self.rect.centerx > 0:
            self.rect.centerx -= self.speed
        else:
            self.rect.centerx = 0

    def move_right(self):
        if self.rect.centerx < self.bounds[0]:
            self.rect.centerx += self.speed
        else:
            self.rect.centerx = self.bounds[0]

    def control(self):
        self.lifetime += 1
        if self.slow_mode:
            self.speed = 2 * self.size_multiplier
        else:
            self.speed = 5 * self.size_multiplier
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1

    def shoot(self, bullets):
        if self.lifetime % 2 == 0:
            # self.shoot_sound.play()
            bullet = PlayerBullet(self.rect.centerx, self.rect.top, self.size_multiplier)
            bullets.add(bullet)

    # TODO bomb
    def bomb(self):
        print('Bomb')

    def draw(self):
        if self.slow_mode:
            self.parent_surface.blit(self.image2, self.rect)
        else:
            self.parent_surface.blit(self.image1, self.rect)

    def update(self, bullets):
        self.listen(bullets)
        self.control()

        # TODO refactor
        self.draw()


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size_multiplier):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load('resources/images/bullet1.png'),
            (int(5 * size_multiplier), int(11 * size_multiplier))
        )
        self.size_multiplier = size_multiplier
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, *args):
        self.rect.centery -= 20 * self.size_multiplier


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, size_multiplier, health):
        pygame.sprite.Sprite.__init__(self)
        self.size_multiplier = size_multiplier
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * size_multiplier
        self.rect.centery = y * size_multiplier
        self.speed = speed
        self.health = health

    def update(self):
        self.rect.centery += self.speed


class SP(Enemy):
    def __init__(self, x, y, speed, size_multiplier):
        Enemy.__init__(self,
                       pygame.transform.scale(
                           pygame.image.load('resources/images/small_enemy.png'),
                           (int(60 * size_multiplier), int(44 * size_multiplier)
                            )
                       ), x, y,
                       speed, size_multiplier, 5)


class MP(Enemy):
    def __init__(self, x, y, speed, size_multiplier):
        Enemy.__init__(self,
                       pygame.transform.scale(
                           pygame.image.load('resources/images/mid_enemy.png'),
                           (int(60 * size_multiplier), int(85 * size_multiplier)
                            )
                       ), x, y,
                       speed, size_multiplier, 5)


class BP(Enemy):
    def __init__(self, x, y, speed, size_multiplier):
        Enemy.__init__(self,
                       pygame.transform.scale(
                           pygame.image.load('resources/images/big_enemy.png'),
                           (int(60 * size_multiplier), int(93 * size_multiplier)
                            )
                       ), x, y,
                       speed, size_multiplier, 5)


class Event:
    def __init__(self, type, tick):
        self.type = type
        self.tick = tick

    def run(self):
        pass


class EnemyEvent(Event):
    def __init__(self, tick, enemy):
        Event.__init__(self, "spawn_enemy", tick)
        self.enemy = enemy

    def run(self):
        return self.enemy


class EventList:
    def __init__(self):
        self.events = []
        self.tick = 0

    def add(self, event):
        self.events.append(event)

    def remove(self, event):
        self.events.remove(event)

    def sort(self):
        self.events.sort(key=lambda event: event.tick)

    def update(self, sprite_group):
        self.tick += 1
        while len(self.events) != 0 and self.events[0].tick == self.tick:
            if self.events[0].type == "spawn_enemy":
                sprite_group.add(self.events[0].run())
                self.events.pop(0)


class STG:
    RUN = 0
    PAUSE = 1
    FAIL = 2

    def __init__(self, size_multiplier=1.0, fullscreen=False):
        pygame.init()

        self.size_multiplier = size_multiplier
        self.width = int(640 * size_multiplier)
        self.height = int(480 * size_multiplier)
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.HWSURFACE)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        self.game_area = pygame.Surface(
            (int(384 * size_multiplier), int(448 * size_multiplier)
             ), pygame.HWSURFACE
        )
        self.bg = pygame.transform.scale(
            pygame.image.load('resources/images/background2.png'),
            (int(384 * size_multiplier), int(448 * size_multiplier)
             )
        )
        self.state = STG.RUN
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('飞机大战 ~ Shoot the Planes')

        self.info_panel = self.get_info_panel()
        self.info_panel_rect = self.info_panel.get_rect()
        self.info_panel_overlay = self.get_info_panel_overlay()
        self.info_panel_overlay_rect = self.info_panel_overlay.get_rect()

        self.player = Player(self.game_area, self.size_multiplier)

        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()

        self.enemy_events = EventList()

        for i in range(1, 24):
            for j in range(1, 4):
                ee = SP(j * 45, -25, j, self.size_multiplier)
                e2e = MP(j * 87, -25, j * 2, self.size_multiplier)
                e3e = BP(j * 163, -25, j * 1.5, self.size_multiplier)
                e = EnemyEvent(i * 103, ee)
                e2 = EnemyEvent(i * 247, e2e)
                e3 = EnemyEvent(i * 493, e3e)
                self.enemy_events.add(e)
                self.enemy_events.add(e2)
                self.enemy_events.add(e3)

        self.enemy_events.sort()

    def run(self):
        while True:
            self.listen()
            if self.state == STG.RUN:
                self.control()

    def listen(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def control(self):
        self.screen.fill((240, 240, 240))
        self.game_area.blit(self.bg, (0, 0))

        self.player.update(self.player_bullets)

        self.enemy_events.update(self.enemies)

        self.enemies.update()
        self.enemies.draw(self.game_area)
        self.player_bullets.update()
        self.player_bullets.draw(self.game_area)

        self.screen.blit(self.game_area, (32 * self.size_multiplier, 16 * self.size_multiplier))
        self.screen.blit(self.info_panel, (432 * self.size_multiplier, 16 * self.size_multiplier))

        self.info_panel_overlay.fill((0, 0, 0, 0))
        self.draw_info()
        self.screen.blit(self.info_panel_overlay, (432 * self.size_multiplier, 16 * self.size_multiplier))

        pygame.display.update()
        self.clock.tick(60)

    def get_info_panel(self):
        info_panel = pygame.Surface(
            (int(192 * self.size_multiplier), int(448 * self.size_multiplier)),
            pygame.SRCALPHA | pygame.HWSURFACE
        )
        rect = info_panel.get_rect()

        diff = txt_img('simhei', int(20 * self.size_multiplier), "Easy", (0, 128, 0))
        dr = diff.get_rect()
        info_panel.blit(diff, (rect.centerx - dr.centerx, 0))

        hiscore = txt_img('simhei', int(15 * self.size_multiplier), "最高得分", (64, 64, 64))
        info_panel.blit(hiscore, (0, 40 * self.size_multiplier))

        score = txt_img('simhei', int(15 * self.size_multiplier), "得分", (0, 0, 0))
        info_panel.blit(score, (0, 60 * self.size_multiplier))

        player = txt_img('simhei', int(15 * self.size_multiplier), "残机", (204, 0, 175))
        info_panel.blit(player, (0, 100 * self.size_multiplier))

        bomb = txt_img('simhei', int(15 * self.size_multiplier), "炸弹", (43, 255, 54))
        info_panel.blit(bomb, (0, 120 * self.size_multiplier))

        power = txt_img('simhei', int(15 * self.size_multiplier), "火力", (250, 100, 0))
        info_panel.blit(power, (0, 200 * self.size_multiplier))

        maxpoint = txt_img('simhei', int(15 * self.size_multiplier), "最大得点", (0, 100, 255))
        info_panel.blit(maxpoint, (0, 220 * self.size_multiplier))

        graze = txt_img('simhei', int(15 * self.size_multiplier), "Graze", (128, 128, 128))
        info_panel.blit(graze, (0, 240 * self.size_multiplier))

        return info_panel

    def get_info_panel_overlay(self):
        info_panel = pygame.Surface(
            (int(192 * self.size_multiplier), int(448 * self.size_multiplier)),
            pygame.SRCALPHA | pygame.HWSURFACE
        )

        return info_panel

    def draw_info(self):
        self.draw_hiscore()
        self.draw_score()
        self.draw_player_count()
        self.draw_bomb_count()
        self.draw_power()
        self.draw_maxpoint()
        self.draw_graze()
        self.draw_fps()

    def draw_hiscore(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{:,}".format(self.player.hiscore), (64, 64, 64))
        info_rect = info.get_rect()
        self.info_panel_overlay.blit(info, (
            (self.info_panel_overlay_rect.width - info_rect.width), 40 * self.size_multiplier))

    def draw_score(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{:,}".format(self.player.score), (0, 0, 0))
        info_rect = info.get_rect()
        self.info_panel_overlay.blit(info, (
            (self.info_panel_overlay_rect.width - info_rect.width), 60 * self.size_multiplier))

    def draw_player_count(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "U", (204, 0, 175))
        for i in range(self.player.lives):
            self.info_panel_overlay.blit(info, (
                (80 + i * 16) * self.size_multiplier, 100 * self.size_multiplier))

    def draw_bomb_count(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "B", (43, 255, 54))
        for i in range(self.player.bombs):
            self.info_panel_overlay.blit(info, (
                (80 + i * 16) * self.size_multiplier, 120 * self.size_multiplier))

    def draw_power(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{0:.2f} / 4.00".format(self.player.power),
                       (250, 100, 0))
        info_rect = info.get_rect()
        self.info_panel_overlay.blit(info, (
            (self.info_panel_overlay_rect.width - info_rect.width), 200 * self.size_multiplier))

    def draw_maxpoint(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{0:,}".format(self.player.maxpoint), (0, 100, 255))
        info_rect = info.get_rect()
        self.info_panel_overlay.blit(info, (
            (self.info_panel_overlay_rect.width - info_rect.width), 220 * self.size_multiplier))

    def draw_graze(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{0:,}".format(self.player.graze), (128, 128, 128))
        info_rect = info.get_rect()
        self.info_panel_overlay.blit(info, (
            (self.info_panel_overlay_rect.width - info_rect.width), 240 * self.size_multiplier))

    def draw_fps(self):
        info = txt_img('simhei', int(16 * self.size_multiplier), "{0:.2f}fps".format(self.clock.get_fps()), (0, 0, 0))
        info_rect = info.get_rect()
        self.screen.blit(info, (
            (640 * self.size_multiplier) - info_rect.width, (480 * self.size_multiplier) - info_rect.height))


class Launcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('192x192')
        self.root.title('飞机大战')
        self.root.resizable(0, 0)
        self.res = tk.LabelFrame(self.root, text='请选择分辨率:', padx=5, pady=5)
        self.m = 1
        MULTIPLIER = [
            ("640x480", '1'),
            ("960x720", '1.5'),
            ("1280x960 (推荐)", '2')
        ]
        self.v = tk.StringVar()
        self.v.set('1')
        for text, value in MULTIPLIER:
            b = tk.Radiobutton(self.res, text=text, variable=self.v, value=value)
            b.pack(anchor=tk.W)

        self.res.pack()

        self.is_fullscreen = tk.IntVar()
        self.is_fullscreen.set(0)
        self.fullscreen = tk.Checkbutton(self.root, text='全屏启动', variable=self.is_fullscreen)

        self.fullscreen.pack()

        self.launch_btn = tk.Button(self.root, text='启动', command=self.launch)
        self.launch_btn.pack()

    def launch(self):
        multiplier = float(self.v.get())
        self.root.destroy()

        # 启动游戏
        stg = STG(multiplier, self.is_fullscreen.get())
        stg.run()


if __name__ == '__main__':
    l = Launcher()
    l.root.mainloop()
