#Sneak

import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize game window etc...
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE + 'FPS : ' + str(self.clock))
        pg.key.set_repeat(500,100)

    def new(self):
        #Reset the Game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat) # (*plat) ---> (plat[0], plat [1], plat[...])
            self.all_sprites.add(p)
            self.platforms.add(p)
        g.run()

    def run(self):
        #Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        #Collisision
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            #escape
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.Jump()

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        # Flip
        pg.display.flip()

    def start_screen(self):
        #Start screen
        pass

    def game_over_screen(self):
        #Game over screen
        pass

g = Game()

g.start_screen()
while g.running :
    g.new()
    g.game_over_screen

pg.quit()
