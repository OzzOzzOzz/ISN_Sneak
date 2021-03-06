#Sneak
import pygame as pg
import random
from os import path
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

    def load_data(self):
        game_folder = path.dirname("__file__")
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt')as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        #Reset the Game
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '*':
                    self.player = Player(self, col, row)
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
        pg.display.set_caption(TITLE + 'FPS : ' + str(self.clock))

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

            for y in range(0, HEIGHT, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            #escape
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_d:
                    PLAYER_ACC = input("ACC: ")
                    PLAYER_FRICTION = input("FRIC: ")
                    PLAYER_GRAV = input("GRAV: ")
                    PLAYER_JUMP = input("JMUP: ")

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
