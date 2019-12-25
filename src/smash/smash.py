#!/usr/bin/env python3
import pygame as pg
import os
import random
from settings import *
from sprites import Platform, Player
from os import path


class Game:
    def __init__(self):
        # pygame
        pg.init()
        pg.mixer.init() # sounds
        pg.display.set_caption("PVP FIGHTING GAME")

        self.screen = pg.display.set_mode((WIDTH, LENGTH))
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.players = pg.sprite.Group()

        # players
        self.player1 = Player(self)
        self.player2 = Player(self)

        self.all_sprites.add(self.player1, self.player2)
        self.players.add(self.player1, self.player2)

        for plat in PLATFORM_LIST:
            self.all_sprites.add(Platform(*plat))
            self.platforms.add(Platform(*plat))

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def draw_shield_bar(self, surf, x, y, percent):
        if percent < 0:
            percent = 0
        BAR_LENGTH = 300
        BAR_HEIGHT = 28
        fill = (percent / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def events(self):
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            self.player1.process_event(event)
            self.player2.process_event(event)

    def update(self):
        self.all_sprites.update()
        # check for player-platform collision
        hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
        if hits:
            if self.player1.vel.y > 0:
                self.player1.pos.y = hits[0].rect.top
                self.player1.vel.y = 0

        hits = pg.sprite.spritecollide(self.player2, self.platforms, False)
        if hits:
            if self.player2.vel.y > 0:
                self.player2.pos.y = hits[0].rect.top
                self.player2.vel.y = 0

        # if player dies 3 times, game over
        if self.player1.lives == 0:
            show_go_screen()

        if self.player2.lives == 0:
            self.player2.kill()

    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.draw_shield_bar(self.screen, 10, 30, self.player1.shield)
        self.draw_text(str(f"HEALTH: {self.player1.shield}"), 18, WHITE, 50, 10)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.running = False



def start_game():
    g = Game()
    g.show_start_screen()

    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()

if __name__ == '__main__':
    start_game()
