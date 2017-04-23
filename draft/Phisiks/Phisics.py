import pygame
from random import *
from pygame.locals import *

pygame.init()

#SETTINGS
display_height = 500
display_width = int(1.6 * display_height)
simon_height = int(display_height / 20 )
simon_width = int(simon_height *.75)

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Phisics')

#LOADS


#VAR_DEF
clock = pygame.time.Clock()

#COLORS
black   = (0,   0,  0)
grey    = (117, 109,109)
white   = (255, 255,255)
red     = (255, 0,  0)
green   = (0,   255 ,0)
blue    = (0,   0,  255)

#CLASS
class Player():
    x, y = 0, 0
    jumping = False
    jump = 10
    gravity = 1
    speed = 5
    color = black
    size = 25

    def draw(self):
        pygame.draw.rect(screen,black,(self.x,self.y,self.size,self.size),2)        

class Hitbox():
    dim = (70,35)
    cord = (0,0)

    def draw(self):
        pygame.draw.rect(screen,
                         black,
                         (self.cord[0],
                          self.cord[1],
                          self.dim[0],
                          self.dim[1]),
                         2)

#FONCTIONS
def do_list(item_list,do):
    for item in item_list:
        if do == 'draw()':
            item.draw()
    
def colision(ax,ay,aw,ah,bx,by,bw,bh):
    return ax < bx+bw and ay < by+bh and bx < ax+aw and by < ay+ah

#def key_detection():
    
    
def game_loop():
    #VARIABLE DEF
    movex, movey = 0, 0

    key_left = False
    key_right = False
    key_up = False

    cubo = Player()
    cubo.x = int(display_width * .1)
    cubo.y = int(display_height * .9) - cubo.size
    
    hitbox_1 = Hitbox()
    hitbox_1.cord = (400, 380)

    hitbox_2 = Hitbox()
    hitbox_2.cord = (550, 330)

    hitbox_3 = Hitbox()
    hitbox_3.cord = (700, 280)

    ground = Hitbox()
    ground.cord = (0,display_height *.9)
    ground.dim = (display_width,50)

    hitbox_list = [ground ,hitbox_1, hitbox_2, hitbox_3]

    while 1:
        #KEY DETECTION
        for event in pygame.event.get():
            #PRESS
            if event.type == pygame.KEYDOWN:
                #LEFT
                if event.key == pygame.K_LEFT:
                    key_left = True
                #RIGHT
                if event.key == pygame.K_RIGHT:
                    key_right = True
                #UP
                if event.key == pygame.K_UP:
                    key_up = True               
                    
            #UNPRESS
            if event.type == pygame.KEYUP:
                #LEFT
                if event.key == pygame.K_LEFT:
                    key_left = False
                #RIGHT
                if event.key == pygame.K_RIGHT:
                    key_right = False
                #UP
                if event.key == pygame.K_UP:
                    key_up = False
                    #ESCAPE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


        #MOVES
        # x
        if key_left and not key_right:
            movex = -cubo.speed
        if key_right and not key_left:
            movex = cubo.speed
        if not key_left and not key_right or key_left and key_right :
            if movex < 0:
                movex += 1
            if movex > 0:
                movex -= 1
     # y
        if key_up and not cubo.jumping:
            cubo.jumping = True
            movey -= cubo.jump
        
        #GRAVITY
        if cubo.jumping :
            movey += cubo.gravity
            
        #BOUNDARIES
        if cubo.x>display_width - cubo.size:
            movex = 0
            cubo.x = display_width - cubo.size
        if cubo.x<0:
            movex = 0
            cubo.x = 0
        if cubo.y > display_height *.9 - cubo.size:
            cubo.jumping = False
            movey = 0
            cubo.y = display_height *.9 - cubo.size

        #DEBUG
        pygame.display.set_caption('Phisic'+str(clock))

        # moving
        cubo.x += movex
        cubo.y += movey

        #DISPLAYS
        screen.fill(grey)
        cubo.draw()
        do_list(hitbox_list,'draw()')
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
