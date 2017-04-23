#Sneak

import pygame as pg
import random
from settings import *

class Game:
    def __init__(self):
        # Initialize game window etc...
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption('FPS : ')
        self.clock = pg.time.Clock()

    def new(self):
        #Reset the Game
        self.all_sprites = pg.sprite.Group()
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

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            #escape
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BLACK)
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
