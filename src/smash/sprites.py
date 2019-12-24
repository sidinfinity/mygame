# sprite classes

import random
import os
import pygame as pg
from settings import *
from smash import *
vec = pg.math.Vector2

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
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.image = pg.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, LENGTH/2)
        self.pos = vec(WIDTH/2, LENGTH/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.lives = 3
        self.fell = False
        self.shield = 100

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -20

    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.jump()

    def update(self):
        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_d]:
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
