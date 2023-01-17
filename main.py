import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
from os import listdir
from time import sleep

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0

IMGS_PATH = 'goose'

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

# ball = pygame.Surface((20, 20))
# ball.fill(WHITE)
player_imgs = [pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(), (100, 60)) for file in listdir(IMGS_PATH)]
ball = player_imgs[0]
ball_rect = ball.get_rect()
ball_speed = 5

bg = pygame.transform.scale(pygame.image.load("background.png").convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bgY = bg.get_width()
bg_speed = 2


def create_enemy():
    #enemy = pygame.Surface((20, 20))
    #enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(), (100, 20))
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_fire(x, y):
    fire = pygame.transform.scale(pygame.image.load("fire.png").convert_alpha(), (600, 600))
    fire_rect = pygame.Rect(x, y, *fire.get_size())
    fire_speed = 0
    return [fire, fire_rect, fire_speed]


def create_bonus():
    #bonus = pygame.Surface((20, 20))
    #bonus.fill(GREEN)
    bonus = pygame.transform.scale(pygame.image.load("bonus.png").convert_alpha(), (50, 100))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

COLLISION = pygame.USEREVENT + 4
pygame.time.set_timer(COLLISION, 0)

enemies = []
bonuses = []
fire = [create_fire(100, 0)]

scores = 0
img_index = 0

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
    
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
    
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            ball = player_imgs[img_index]
        
        #if event.type == COLLISION:
                   
    pressed_keys = pygame.key.get_pressed()

    # main_surface.fill(WHITE)

    #main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(ball, (ball_rect))

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))    

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            main_surface.blit(fire[0][0],fire[0][1])
            # create_fire(50, 50)
            #sleep(10)
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        #print(len(bonuses))

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))
            #print(len(bonuses))
            
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
            #print(scores)

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_UP] and not ball_rect.top < 0:
        ball_rect = ball_rect.move(0, - ball_speed)

    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_keys[K_LEFT] and not ball_rect.left < 0:
        ball_rect = ball_rect.move( - ball_speed, 0)
    
    #if ball_rect.bottom >= height or ball_rect.top <= 0:
        #ball.fill(GREEN)
        #ball_speed = - ball_speed
    
    #if ball_rect.right >= width or ball_rect.left <= 0:
        #ball.fill(RED)
        #ball_speed = - ball_speed
        
    
    #main_surface.fill((155, 155, 155))
    pygame.display.flip()
