#INIT
import pygame
from random import *
pygame.init()

#SETTINGS
display_width = 500
display_height = int((16/9)*display_width)
car_width = 60
car_height = 100
cone_width = 64
cone_height = 66
road_width = 500
road_height = 900


#COLOR
grey = (117, 109, 109)
black = (0,0,0)
white = (255,255,255)

#PYGAME
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Watuuure')
clock = pygame.time.Clock()

#IMAGE LOAD
carimg = pygame.image.load('car.png')
coneimg = pygame.image.load('cone.png')
roadimg = pygame.image.load('road.png')

#FUNCTION
def cone(conex, coney):
    gameDisplay.blit(coneimg,(conex,coney))

def road(x,y):
    gameDisplay.blit(roadimg,(x,y))
    gameDisplay.blit(roadimg,(x,y-road_height)) 

def display_speed(n):
    font = pygame.font.SysFont(None, 25)
    text = font.render("SPEED: "+str(n) + ' KM/H', True, black)
    gameDisplay.blit(text,(display_width * 0.7 ,0))

def display_score(n):
    font = pygame.font.SysFont(None, 25)
    text = font.render("SCORE: "+str(n), True, black)
    gameDisplay.blit(text,(0,0))

def collision(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx+bw and ay < by+bh and bx < ax+aw and by < ay+ah

def car(x,y):
    gameDisplay.blit(carimg,(x,y))

def game_loop():
    #DEF VAR
    x = (display_width * 0.45)
    y = (display_height * 0.85)
    vroumval = 0
    vroumway = 'down'
    x_change = 0
    crashed = False
    background_color = grey
    cone_here = False
    speed = 5
    score_val = 0

    ##EVENT LOOP
    while 1:
        for event in pygame.event.get():

            #KEY CONTROL
            if event.type == pygame.KEYDOWN:
                #ESCAPE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT:
                    if x > 0 + speed:
                        x_change = -speed
                    else:
                        x = 0
                if event.key == pygame.K_RIGHT:
                    if x < display_width - car_width - speed:
                        x_change = speed
                    else:
                        x = display_width - car_width
            #KEY UP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    x_change = 0

        #CONE
        if not cone_here:
            conex = randint(0,display_width-cone_width)
            coney = -100
            cone_here = True

        #ANIM
        if vroumway == 'up':
            vroumval -= 1
            if vroumval == 0:
                vroumway = 'down'
                y += 2

        if vroumway == 'down':
            vroumval += 1
            if vroumval == 10:
                vroumway = 'up'
                y -= 2
        
        #BOUNDARIES
        if x > display_width - car_width :
            x = display_width - car_width - speed
        if x < 0:
            x = 0 + speed
        
        if coney > display_height :
            cone_here = False
            score_val += 1
            if speed < 40:
                speed += 0.5

        #MOVING
        x+= x_change
        coney += speed

        #CRASH
        if collision(x, y, car_width, car_height, conex, coney, cone_width, cone_height):
            space_press = False
            print('crash')
            while not space_press:
                font = pygame.font.SysFont(None, 25)
                text = font.render("PRESS SPACE TO RETRY", True, black)
                gameDisplay.blit(text,(display_width * 0.3 ,display_height * 0.47))
                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        space_press = True
                            
            game_loop()

        #REFRESH
        road(0,coney)
        #
        display_speed(speed)
        display_score(score_val)
        cone(conex,coney)
        car(x,y)
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
