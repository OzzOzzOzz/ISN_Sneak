import pygame as pg
from settings import *
from random import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def Jump(self):
        '''
        #jump if on platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -=1
        if hits:
        '''
        print('JUMP')
        self.vel.y = -PLAYER_JUMP

    def collide_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                print('collide x')
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                print('collide y')
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def get_keys(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC



    def update(self):
        self.get_keys()

        # apply friction
        self.acc.x = self.acc.x + self.vel.x * PLAYER_FRICTION
        # motion equation
        self.vel = (self.vel + self.acc)
        self.pos = self.pos + self.vel + 0.5 * self.acc


        self.rect.x = self.pos.x
        self.collide_walls('x')
        self.rect.y = self.pos.y
        self.collide_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        r1 = randint(0, 255)
        self.image.fill((0, r1, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
