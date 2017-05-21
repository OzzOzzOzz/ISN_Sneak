import pygame as pg
from settings import *
from random import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #Grab an image out of a spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.walking = False
        self.jumping = False
        self.can_jump = False
        self.can_doublejump = False
        self.can_grap = False
        self.can_sneak = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.double_jump = True

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(32, 0, 32, 32),
                                self.game.spritesheet.get_image(0, 0, 32, 32)]
        self.walk_frames_r = [self.game.spritesheet.get_image(32, 0, 32, 32),
                                self.game.spritesheet.get_image(0, 0, 32, 32)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(64, 0, 32, 32)

    def Jump(self):
        #jump if on platform

        if self.can_jump:
            if self.on_ground():
                self.vel.y = -PLAYER_JUMP
                self.jumping = True
                self.double_jump = True
            elif self.double_jump and self.can_doublejump:
                self.vel.y = -PLAYER_JUMP
                self.jumping = True
                self.double_jump = False

    def collide_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def get_keys(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

    def on_ground(self):
        self.rect.y += 1
        hit = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.y -=1
        return hit

    def update(self):
        self.get_keys()
        self.animate()
        # apply friction
        self.acc.x = self.acc.x + self.vel.x * PLAYER_FRICTION
        # motion equation
        if abs(self.vel.x) < 0.3:
            self.vel.x = 0
        self.vel = (self.vel + self.acc)
        self.pos = self.pos + self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        self.collide_walls('x')
        self.rect.y = self.pos.y
        self.collide_walls('y')

        if self.on_ground():
            self.jumping = False
            self.double_jump = True

        if self.pos.x > WIDTH - TILESIZE/2:
            self.pos.x = 0
            self.game.scroll('right')
            print('RIGHT')

        if self.pos.x < 0:
            self.pos.x = WIDTH - TILESIZE
            self.game.scroll('left')
            print('LEFT')

        if self.pos.y > HEIGHT - TILESIZE/2:
            self.pos.y = 0
            self.game.scroll('up')
            print('UP')

        if self.pos.y < 0:
            self.pos.y = HEIGHT - TILESIZE
            self.game.scroll('down')
            print('DOWN')

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping:
            if now - self.last_update > 600:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, pixelcolor):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wallsheet.get_image(32, 32, 32, 32)
        if pixelcolor == UPPER_LEFT:
            self.image = self.game.wallsheet.get_image(0, 0, 32, 32)
        if pixelcolor == UP:
            self.image = self.game.wallsheet.get_image(32, 0, 32, 32)
        if pixelcolor == UPPER_RIGHT:
            self.image = self.game.wallsheet.get_image(64, 0, 32, 32)
        if pixelcolor == LEFT:
            self.image = self.game.wallsheet.get_image(0, 32, 32, 32)
        if pixelcolor == CENTER:
            self.image = self.game.wallsheet.get_image(32, 32, 32, 32)
        if pixelcolor == RIGHT:
            self.image = self.game.wallsheet.get_image(64, 32, 32, 32)
        if pixelcolor == BUTTOM_LEFT:
            self.image = self.game.wallsheet.get_image(0, 64, 32, 32)
        if pixelcolor == BUTTOM:
            self.image = self.game.wallsheet.get_image(32, 64, 32, 32)
        if pixelcolor == BUTTOM_RIGHT:
            self.image = self.game.wallsheet.get_image(64, 64, 32, 32)
        if pixelcolor == COLUMN_UP:
            self.image = self.game.wallsheet.get_image(96, 0, 32, 32)
        if pixelcolor == COLUMN_CENTER:
            self.image = self.game.wallsheet.get_image(96, 32, 32, 32)
        if pixelcolor == COLUMN_DOWN:
            self.image = self.game.wallsheet.get_image(96, 64, 32, 32)
        if pixelcolor == ROW_LEFT:
            self.image = self.game.wallsheet.get_image(0, 96, 32, 32)
        if pixelcolor == ROW_CENTER:
            self.image = self.game.wallsheet.get_image(32, 96, 32, 32)
        if pixelcolor == ROW_RIGHT:
            self.image = self.game.wallsheet.get_image(64, 96, 32, 32)
        if pixelcolor == ALONE:
            self.image = self.game.wallsheet.get_image(96, 96, 32, 32)
        if pixelcolor == ANGLE_BUTTOM_RIGHT:
            self.image = self.game.wallsheet.get_image(128, 0, 32, 32)
        if pixelcolor == ANGLE_BUTTOM_LEFT :
            self.image = self.game.wallsheet.get_image(160, 0, 32, 32)
        if pixelcolor == ANGLE_UPPER_RIGTH:
            self.image = self.game.wallsheet.get_image(128, 32, 32, 32)
        if pixelcolor == ANGLE_UPPER_LEFT:
            self.image = self.game.wallsheet.get_image(160, 32, 32, 32)
        if pixelcolor == BORDERED_ANGLE_UPPER_LEFT:
            self.image = self.game.wallsheet.get_image(128, 64, 32, 32)
        if pixelcolor == BORDERED_ANGLE_UPPER_RIGHT:
            self.image = self.game.wallsheet.get_image(160, 64, 32, 32)
        if pixelcolor == BORDERED_ANGLE_BUTTOM_LEFT:
            self.image = self.game.wallsheet.get_image(128, 96, 32, 32)
        if pixelcolor == BORDERED_ANGLE_BUTTOM_RIGHT:
            self.image = self.game.wallsheet.get_image(160, 96, 32, 32)
        self.image.set_colorkey(CANAL_ALPHA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y, pixelcolor):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if pixelcolor == POWERUP_JUMP:
            self.type = 'jump'
            self.image = self.game.powsheet.get_image(0, 0, 32, 32)
        if pixelcolor == POWERUP_DOUBLEJUMP:
            self.type = 'doublejump'
            self.image = self.game.powsheet.get_image(32, 0, 32, 32)
        if pixelcolor == POWERUP_GRAP:
            self.type = 'grap'
            self.image = self.game.powsheet.get_image(64, 0, 32, 32)
        if pixelcolor == POWERUP_SNEAK:
            self.type = 'sneak'
            self.image = self.game.powsheet.get_image(96, 0, 32, 32)
        self.image.set_colorkey(CANAL_ALPHA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
