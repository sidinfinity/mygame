#!/usr/bin/env python3
import pygame
import os
import random
from os import path

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 225, 0)
WIDTH = 1204      # width for gaming screen
LENGTH = 806      # length for gaming screen
BALL_MOVE = 6
LINE_MOVE = 5
ASSET_FOLDER     = "assets/Pong_graphics"

# set up assets folder

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, LENGTH / 2)
        self.x = BALL_MOVE
        self.y = BALL_MOVE
        if random.randint(0, 100) % 2 == 0:
            self.x *= -1
        if random.randint(0, 100) % 2 == 0:
            self.y *= -1

    def turn_right(self):
        self.x = BALL_MOVE

    def turn_left(self):
        self.x = -1 * BALL_MOVE

    def update(self):
        self.rect.x += self.x
        self.rect.y += self.y
        if self.rect.y >= LENGTH:
            self.y = -1 * BALL_MOVE

        if self.rect.x >= WIDTH:
            pygame.quit()

        if self.rect.x <= 0:
            pygame.quit()

        if self.rect.y <= 0:
            self.y = BALL_MOVE


class Line(pygame.sprite.Sprite):
    def __init__(self, file, is_left, x = 10, y = 10):
        self.file = file
        self.is_left = is_left
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        game_folder = path.join(path.dirname(__file__))
        self.image = pygame.image.load(
            os.path.join(game_folder, ASSET_FOLDER, self.file)
        ).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        key = pygame.key.get_pressed()

        if self.rect.top < 0:
            self.rect.y += 1
            return

        if self.rect.bottom > LENGTH:
            self.rect.y -= 1
            return

        if not self.is_left:
            if key[pygame.K_UP]:
                self.rect.y -= LINE_MOVE
            if key[pygame.K_DOWN]:
                self.rect.y += LINE_MOVE
        else:
            if key[pygame.K_w]:
                self.rect.y -= LINE_MOVE
            if key[pygame.K_s]:
                self.rect.y += LINE_MOVE


def init_pygame():
    FPS = 45          # frames per second (how fast the screen refreshes)
    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()  # for sound
    screen = pygame.display.set_mode((WIDTH, LENGTH))
    pygame.display.set_caption("Game Skeleton")
    clock = pygame.time.Clock()

    left_sprites = pygame.sprite.Group()
    right_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    ball = Ball()
    line1 = Line("line1.png", True, 100, LENGTH / 2)
    line2 = Line("line2.png", False, WIDTH - 100, LENGTH / 2)

    left_sprites.add(line1)
    right_sprites.add(line2)

    all_sprites.add(line1)
    all_sprites.add(line2)
    all_sprites.add(ball)

    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # detect left collision
        if pygame.sprite.spritecollide(ball, left_sprites, False):
            ball.turn_right()

        # detect right collision
        if pygame.sprite.spritecollide(ball, right_sprites, False):
            ball.turn_left()


        # Draw / render
        screen.fill(WHITE)
        all_sprites.draw(screen)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()



if __name__ == '__main__':
    init_pygame()
