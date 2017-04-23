import pygame
from random import *
from pygame.locals import *

pygame.init()

#SETTINGS
display_height = 500
display_width = int(1.6 * display_height)
simon_height = int(display_height / 20 )
simon_width = int(simon_height *.75)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Simon')

#LOADS
simonimg = pygame.image.load("simon.png")
simonimg = pygame.transform.scale(simonimg,(simon_width,simon_height))
backgroundimg = pygame.image.load("background.png")
backgroundimg = pygame.transform.scale(backgroundimg,(display_width,display_height))

#VAR_DEF
clock = pygame.time.Clock()

#COLORS
black = (0,0,0)
grey = (117, 109, 109)
white = (255,255,255)

#CLASS
#class Player():
    

class Hitbox():
    dim = (70,35)
    cord = (0,0)

    def draw_hit(self):
        pygame.draw.rect(gameDisplay,
                         black,
                         (self.cord[0],
                          self.cord[1],
                          self.dim[0],
                          self.dim[1]),
                         2)

#FONCTIONS
def simon(x,y):
    gameDisplay.blit(simonimg,(x,y))

def do_list(item_list,do):
    for item in item_list:
        if do == 'draw_hit()':
            item.draw_hit()
        
def background():
    gameDisplay.blit(backgroundimg,(0,0))
    
def colision(ax,ay,aw,ah,bx,by,bw,bh):
    return ax < bx+bw and ay < by+bh and bx < ax+aw and by < ay+ah

def colix(ax,aw,bx,bw,):
    return ax < bx+bw and bx < ax+aw

def coley(ay,ah,by,bh):
    return ay < by+bh and by < ay+ah
    
def game_loop():
    #VARIABLE DEF
    movex = 0
    movey = 0
    x = display_width * .1
    y = display_height * .5
    jumping = True
    jump = 10
    gravity = .5
    speed = 4

    hitbox_0 = Hitbox()
    hitbox_0.cord = (250, 430)
    
    hitbox_1 = Hitbox()
    hitbox_1.cord = (400, 380)

    hitbox_2 = Hitbox()
    hitbox_2.cord = (550, 330)

    hitbox_3 = Hitbox()
    hitbox_3.cord = (700, 280)

    ground = Hitbox()
    ground.cord = (0,display_height *.9)
    ground.dim = (display_width,50)

    hitbox_list = [ground ,hitbox_0,hitbox_1, hitbox_2, hitbox_3,]

    while 1:
        #KEY DETECTION
        for event in pygame.event.get():
            #PRESS
            if event.type == pygame.KEYDOWN:
                #LEFT
                if event.key == pygame.K_LEFT :
                    movex = -speed

                #RIGHT
                if event.key == pygame.K_RIGHT :
                    movex = speed
                
                #UP
                if event.key == pygame.K_UP:
                    jumping = True
                    movey -= jump

            #UNPRESS
            if event.type == pygame.KEYUP:
                #LEFT RIGHT
                if event.key == pygame.K_LEFT :
                    movex = 0

                if event.key == pygame.K_RIGHT:
                    movex = 0

                #ESCAPE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    game_loop()

            #DEBUG
        pygame.display.set_caption('Simon'+str(clock))

        if colision(x,y,simon_width,simon_height,
                     hitbox_0.cord[0],hitbox_0.cord[1],hitbox_0.dim[0],hitbox_0.dim[1]):
            
            if colix(x,simon_width,
                     hitbox_0.cord[0],hitbox_0.dim[0]):
                movex = 0
            if coley(y,simon_height,
                     hitbox_0.cord[1],hitbox_0.dim[1]):
                movey = 0
        #MOVES
        x += movex
        y += movey
        
        #GRAVITY
        if jumping:
            movey += gravity

        #BOUNDARIES
        if x>display_width - simon_width:
            movex = 0
            x = display_width - simon_width
        if x<0:
            movex = 0
            x = 0
        if y > display_height *.9 - simon_height:
            movey = 0
            y = display_height *.9 - simon_height
            
        #COLISION
        if do_list(hitbox_list,'colision()'):
            movey = 0



        #DISPLAYS
        background()
        do_list(hitbox_list,'draw_hit()')
        simon(x,y)
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
