#!/usr/bin/env python3
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Graphics by Kenney on opengameart.org
# Code from kidscancode.org 

import pygame
import random
from os import path
import os
import sys

GAME_FOLDER = path.join(path.dirname(__file__))
WIDTH = 480
HEIGHT = 600
FPS = 60

NUMBER_OF_MOBS = 10
PLAYER_SPEED = 5
GREEN = (0, 225, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_shield_bar(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_text(surf, text, size, x , y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, file1, x, y):
        self.file1 = file1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(GAME_FOLDER, self.file1, 'laserRed16.png')
        ).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10



    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, file1):
        self.file1 = file1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(GAME_FOLDER, self.file1, 'playerShip1_red.png')
        ).convert()
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speedx = -1 * PLAYER_SPEED
        if key[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        self.rect.x  += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet('assets/SpaceShooterRedux/PNG/Lasers', self.rect.centerx, self.rect.top)
        return bullet

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self, meteor_images):
        self.meteor_images = meteor_images
        pygame.sprite.Sprite.__init__(self)
        self._image_orig = random.choice(self.meteor_images)
        self._image_orig.set_colorkey(BLACK)
        self.image = self._image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self._image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10      \
                or self.rect.left < -25     \
                or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim = explosion_anim
        self.size = size
        self.image = self.explosion_anim[self.size][0]
        self.rect  = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



def start_game():

    def show_go_screen():
        draw_text(screen, "SHUMP!", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH/ 2, HEIGHT / 2)
        draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYUP:
                    waiting = False

    background = pygame.image.load(
        os.path.join(
            GAME_FOLDER, 'assets/SpaceShooterRedux/Backgrounds/' 'starfield.png'
        )
    ).convert()
    background_rect = background.get_rect()






    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
                   'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
                   'meteorBrown_tiny1.png'
                   ]

    meteor_images = [pygame.image.load(
            os.path.join(
                GAME_FOLDER, 'assets/SpaceShooterRedux/PNG/Meteors', img
            )
        ).convert() for img in meteor_list]

    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    for i in range(9):
        filename = f'regularExplosion0{i}.png'
        img = pygame.image.load(os.path.join(
                GAME_FOLDER, 'assets/SpaceShooterRedux/Explosions', filename)
            ).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)

    shoot_sound = pygame.mixer.Sound(os.path.join(
            GAME_FOLDER, 'assets/Sounds', 'Laser_Shoot1.wav')
        )

    explosion_sound = pygame.mixer.Sound(os.path.join(
            GAME_FOLDER, 'assets/Sounds', 'Explosion1.wav')
        )

    pygame.mixer.music.load(os.path.join(
            GAME_FOLDER, 'assets/Sounds', 'backgroundMusic1.ogg')

        )
    pygame.mixer.music.set_volume(1.0)



    def newmob():
        m = Mob(meteor_images)
        all_sprites.add(m)
        mobs.add(m)


    score = 0
    pygame.mixer.music.play(loops = -1)
    # Game loop
    game_over = True
    running = True
    while running:
        if game_over:
            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player('assets/SpaceShooterRedux/PNG')
            all_sprites.add(player)
            player_mini_img = pygame.transform.scale(player.image, (25, 19))

            for i in range(NUMBER_OF_MOBS):
                newmob()

        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()

        # Update
        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            explosion_sound.play()
            score += 50 - hit.radius
            expl = Explosion(hit.rect.center, 'lg', explosion_anim)
            all_sprites.add(expl)
            # create a new mob and add to 2 sprite groups (mobs and all_sprites)
            newmob()


        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            explosion_sound.play()
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm', explosion_anim)
            all_sprites.add(expl)
            newmob()
            if player.shield <= 0:
                explosion_sound.set_volume(5.0)
                explosion_sound.play()
                explosion_sound.set_volume(0.5)

                death_explosion = Explosion(player.rect.center, 'lg', explosion_anim)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100


        if player.lives == 0 and not death_explosion.alive():
            game_over = True


        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    start_game()
