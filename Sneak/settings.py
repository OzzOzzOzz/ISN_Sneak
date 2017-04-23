# Game option
TITLE = 'Jumpy !'
WIDTH = 720
HEIGHT = 480
FPS = 60

#Player properties
PLAYER_ACC = .5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8

#Starting platforrm
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                (WIDTH/2 - 50, HEIGHT * 3 / 4, 100, 20),
                (125, HEIGHT-350,100,20),
                (350, 100, 50,20)
                ]

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
