# sprite classes

import random
import os
import pygame as pg
from settings import *


class Platform(pg.sprite.Sprite):
    def __init__(self, width, length, x, y):
        super(Platform, self).__init__()
        self.image = pg.Surface((width, length))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class Player(pg.sprite.Sprite):
    def __init__(self, controls, name):
        super(Player, self).__init__()
        self.vec = pg.math.Vector2
        self.controls = controls
        self.image = pg.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, LENGTH/2)
        self.pos = self.vec(WIDTH/2, LENGTH/2)
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.lives = 3
        self.fell = False
        self.shield = 100
        self.name = name

        self._platform_group = None

    @property
    def platform_group(self):
        return self._platform_group

    @platform_group.setter
    def platform_group(self, platforms):
        self._platform_group = platforms

    def jump(self):
        hits = pg.sprite.spritecollide(self, self._platform_group, False)
        if hits:
            self.vel.y = -20

    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.controls['jump']:
                self.jump()

    def update(self):
        self.acc = self.vec(0, GRAVITY)
        keys = pg.key.get_pressed()

        if keys[self.controls['left']]:
            self.acc.x = -PLAYER_ACC

        if keys[self.controls['right']]:
            self.acc.x = PLAYER_ACC

        # applies friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        # checking is player leaves screan
        if self.rect.centerx > WIDTH or self.rect.centerx < 0:
            self.pos = (WIDTH / 2, LENGTH / 2 - 100)
            self.fell = True

        if self.rect.centery > LENGTH or self.rect.centery < 0:
            self.pos = (WIDTH / 2, LENGTH / 2 - 100)
            self.fell = True

        # deducting lives
        if self.fell:
            self.lives -= 1
            self.fell = False
