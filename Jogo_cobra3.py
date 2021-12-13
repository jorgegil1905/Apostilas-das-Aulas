import pygame, random
import winsound
from pygame.locals import *

def on_grid_random():
    x = random.randint(0,590)
    y = random.randint(0,590)
    return (x//10 * 10, (y//10 * 10) + 40)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
PLACAR = 0

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((0,0,255))

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))

apple_pos2 = on_grid_random()
apple2 = pygame.Surface((10,10))
apple2.fill((0,255,0))

my_direction = LEFT

clock = pygame.time.Clock()

while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT

    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0,0))
        winsound.Beep(1000,100)
        PLACAR = PLACAR + 10

    if collision(snake[0], apple_pos2):
        apple_pos2 = on_grid_random()
        snake.append((0,0))
        winsound.Beep(1000,100)
        PLACAR = PLACAR + 20

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
        
    
    if my_direction == UP:
        if snake[0][1] < 41:
            if snake[0][0] < 200:
                snake[0] = (snake[0][0] + 10, snake[0][1])
                my_direction = RIGHT
                continue
            else:
                snake[0] = (snake[0][0] - 10, snake[0][1])
                my_direction = LEFT
                continue
        else:
            snake[0] = (snake[0][0], snake[0][1] - 10)  

    if my_direction == DOWN:
        if snake[0][1] > 580:
            if snake[0][0] < 200:
                snake[0] = (snake[0][0] , snake[0][1])
                my_direction = RIGHT
            else:
                    snake[0] = (snake[0][0] , snake[0][1])
                    my_direction = LEFT
        else:
            snake[0] = (snake[0][0], snake[0][1] + 10)  
        
    if my_direction == LEFT:
        if snake[0][0] < 10:
            if snake[0][1] < 200:
                snake[0] = (snake[0][0], snake[0][1] + 10 )
                my_direction = DOWN
            else:
                snake[0] = (snake[0][0], snake[0][1] - 10 )
                my_direction = UP
        else:
            snake[0] = (snake[0][0] - 10, snake[0][1] )  
    
    if my_direction == RIGHT:
        if snake[0][0] > 580:
            if snake[0][1] < 200:
                snake[0] = (snake[0][0], snake[0][1] + 10 )
                my_direction = DOWN
            else:
                snake[0] = (snake[0][0], snake[0][1] - 10 )
                my_direction = UP
        else:
            snake[0] = (snake[0][0] + 10, snake[0][1] )  
    
   
    screen.fill((192,192,192))
    screen.blit(apple, apple_pos)
    screen.blit(apple2, apple_pos2)

    for pos in snake:
        screen.blit(snake_skin,pos)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        TEXTO = '    Jogo do Guinomo Guto Placar : ' + str(PLACAR)
        textsurface = myfont.render(TEXTO, False, (255, 0, 0))
        screen.blit(textsurface,(0,0))

    pygame.display.update()
