import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def Jump(self):
        #jump if on platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -=1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x = self.acc.x + self.vel.x * PLAYER_FRICTION
        # motion equation
        self.vel = self.vel + self.acc
        self.pos = self.pos + self.vel + 0.5 * self.acc
        # Screen border
        if self.pos.x > WIDTH:
            self.pos.x = 0
            print('scroll right')
        if self.pos.x < 0:
            self.pos.x = WIDTH
            print('scroll left')

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#3:14
'''
Mega site: mega.nz/
Link: #!guxRDBBQ
Key: !v07RWa5tXAgJy_RFCRgktVgpm4d0LVmpMPZlWjT6HE0
'''
