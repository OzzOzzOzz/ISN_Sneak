#Sneak
import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize game window etc...
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE + 'FPS : ' + str(self.clock))
        self.running = True
        self.font_name = pg.font.match_font('FONT_NAME')
        pg.key.set_repeat(500,100)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname("__file__")
        self.img_dir = path.join(self.dir, "img")
        self.mapsheet = Spritesheet(path.join(self.img_dir, MAPSHEET))
        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET))
        self.wallsheet = Spritesheet(path.join(self.img_dir, WALLSHEET))
        self.MAP_X = SPAWNMAP[0]
        self.MAP_Y = SPAWNMAP[1]

    def generate_level(self, map_img):
        self.screen.blit(map_img,(0,0))
        for row in range(int(HEIGHT / TILESIZE)):
            for col in range(int(WIDTH / TILESIZE)):
                pixelcolor = self.screen.get_at((col, row))
                if pixelcolor == SPAWN and self.new:
                    self.new = False
                    self.player = Player(self, col, row)
                elif pixelcolor != WHITE and pixelcolor != SPAWN:
                    Wall(self, col, row, pixelcolor)

    def scroll(self,way):
        if way == 'right':
            self.MAP_X += 1
        if way == 'left':
            self.MAP_X -= 1
        if way == 'up':
            self.MAP_Y += 1
        if way == 'down':
            self.MAP_Y -= 1

        self.all_sprites.remove(self.walls)
        self.walls.empty()

        self.generate_level(self.mapsheet.get_image(self.MAP_X * 32, self.MAP_Y * 24, 32, 24))


    def new(self):
        #Reset the Game
        self.new = True
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        self.generate_level(self.mapsheet.get_image(self.MAP_X * 32, self.MAP_Y * 24, 32, 24))

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
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.Jump()
                if event.key == pg.K_r:
                    self.new()
                if event.key == pg.K_p:
                    print(self.walls)

    def start_screen(self):
        #Start screen
        self.screen.fill(BLACK)
        self.draw_text("Welcome to :  " + TITLE, 72, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to start", 80, WHITE, WIDTH / 2, HEIGHT * 2.2 / 4)
        pg.display.flip()
        self.wait_for_key()

    def game_over_screen(self):
        #Game over screen
        pass

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    running = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.start_screen()
while g.running :
    g.new()
    g.game_over_screen

pg.quit()
