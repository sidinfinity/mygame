# sprite classes

import random
import os
import pygame as pg
from settings import *
from weapons import Pistol
vec = pg.math.Vector2


class Platform(pg.sprite.Sprite):
    def __init__(self, screen, width, length, x, y):
        super(Platform, self).__init__()
        self.image = pg.Surface((width, length))
        self.image.fill(BLACK)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def draw(self):
        pass


class Player(pg.sprite.Sprite):
    def __init__(self, controls, screen, name, color=BLUE):
        super(Player, self).__init__()
        self.controls = controls
        self.screen = screen
        self.image = pg.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, LENGTH/2)
        self.pos = vec(WIDTH/2, LENGTH/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.lives = 3
        self.fell = False
        self.shield = 100
        self.name = name
        self.direction = None
        self._platform_group = None
        self.weapon = Pistol(self.controls, self.screen)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.weapon)

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

    def gun_update(self):
        self.weapon.shoot()
        if self.direction == 'left':
            self.weapon.rect.right = self.rect.centerx

        else:
            self.weapon.rect.left = self.rect.centerx

        self.weapon.rect.centery = self.rect.centery

    def update(self):
        # gun update
        self.gun_update()

        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()

        if keys[self.controls['left']]:
            self.acc.x = -PLAYER_ACC
            self.direction = 'left'

        if keys[self.controls['right']]:
            self.acc.x = PLAYER_ACC
            self.direction = 'right'

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

    def draw(self):
        # draws sprites contained in players
        print("draw player sprites")

        self.all_sprites.draw(self.screen)
        # call draw() method for all sprite objects
        for sprite in self.all_sprites:
            sprite.draw()
