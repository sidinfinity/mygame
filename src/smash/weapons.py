import pygame as pg
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pg.Surface((5,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.rect.x+=5
        print("firing bullet")
        if pg.time.get_ticks() - self.spawn_time >= 3000:
            self.kill()

        if self.rect.centerx >= WIDTH or self.rect.centery >= 0:
            self.kill()

    def draw(self):
        pass


class Weapon(pg.sprite.Sprite):
    def __init__(self, screen):
        super(Weapon, self).__init__()
        self.screen = screen

    def draw(self):
        raise NotImplementedError

    def shoot(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class Pistol(Weapon):
    def __init__(self, controls, screen):
        super(Pistol, self).__init__(screen)
        self.controls = controls
        self.image = pg.Surface((30, 10))
        self.image.fill(PURPLE)
        self.controls = controls
        self.rect = self.image.get_rect()
        self.all_sprites = pg.sprite.Group()

    def shoot(self):
        keys = pg.key.get_pressed()
        if keys[self.controls['shoot']]:
            self.all_sprites.add(Bullet())

    def update(self):
        # update bullet movements
        self.all_sprites.update()


    def draw(self):
        print("pistol draw")

        self.all_sprites.draw(self.screen)
        # call draw() method for all sprite objects
        for sprite in self.all_sprites:
            sprite.draw()
