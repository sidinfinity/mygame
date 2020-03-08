import pygame as pg
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, direction):
        super(Bullet, self).__init__()
        self.image = pg.Surface((15,7))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if self.direction is None:
            return
        if self.direction == "left":
            self.rect.x += -5
        else:
            self.rect.x += 5
        '''
        if pg.time.get_ticks() - self.spawn_time >= 3000:
            self.kill()

        if self.rect.centerx >= WIDTH or self.rect.centery >= 0:
            self.kill()
        '''

    def draw(self):
        pass


class Weapon(pg.sprite.Sprite):
    def __init__(self, screen):
        super(Weapon, self).__init__()
        self.screen = screen
        self._direction = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if direction == "left" or direction == "right":
            self._direction = direction
        else:
            self._direction = None

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
            self.bullet = Bullet(self.direction)
            self.bullet.rect.center = self.rect.center
            self.all_sprites.add(self.bullet)

    def update(self):
        # update bullet movements
        self.all_sprites.update()

        # shooting
        self.shoot()





    def draw(self):

        self.all_sprites.draw(self.screen)
        # call draw() method for all sprite objects
        for sprite in self.all_sprites:
            sprite.draw()
