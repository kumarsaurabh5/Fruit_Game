import pygame, sys
import os
import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

player_lives = 3
score = 0
fruits = ['melon', 'orng', 'app', 'guava', 'bomb']

# initialize pygame and create window

WIDTH = 1000
HEIGHT = 600
FPS = 10
cap=cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FPS, 1)
detector=HandDetector(detectionCon=0.65, maxHands=1)
pygame.init()
pygame.display.set_caption('Fruit-Ninja')
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Define colors

WHITE = (255,255,255) 
BLACK = (0,0,0) 
RED = (255,0,0) 
GREEN = (0,255,0) 
BLUE = (0,0,255)

background = pygame.image.load('./img/bg.jpg')                                  #game background
background1 = pygame.image.load('./img/bg1.jpg')                                  #game background
background2 = pygame.image.load('./img/bg2.jpg')                                  #game background
font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts/PDBI.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255,0,0))    #score display
lives_icon = pygame.image.load('./img/w_h.png')                    #images that shows remaining lives

# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "img/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,700),
        'y' : 800,
        'speed_x': random.randint(-10,10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# Dictionary to hold the data the random fruit generation

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("./img/r_h.png"), (x, y))

# Generic method to draw fonts on the screen

font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# draw players lives

def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background1, (0,0))
    # draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        gameDisplay.blit(background1, (0,0))
        draw_text(gameDisplay,"Score : " + str(score), 100, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH/2 , HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game Loop
first_round = True
game_over = True
game_running = True
while game_running :
    Success, img=cap.read()
    img=cv2.flip(img,1)
    hands, img=detector.findHands(img)
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, './img/r_h.png')
        score = 0

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.K_q:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, './img/r_h.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            if hands:
                print(len(hands))
                hand=hands[0]
                print(hand)
                current_position=(hand["lmList"][5:9])
                # current_position=np.array(current_position)
                x_list=sorted([l[0] for l in current_position])
                y_list=sorted([l[1] for l in current_position])
                # print('list: ',current_position)
                gameDisplay.blit(pygame.image.load('./img/knife.png'),current_position[0][:2])
                # print(x_list)
                # print(y_list)
            else:
                current_position=[[5,8]]
                x_list=[5]
                y_list=[8]

            # pygame.draw.circle(gameDisplay, BLUE, current_position, 5) #isme dekhna

            if not value['hit'] and x_list[0]-50 < value['x'] and x_list[-1]+50 > value['x'] \
                and y_list[0]-50 < value['y'] and y_list[-1]+50 > value['y']:
            # if not value['hit']:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)

                    if player_lives < 0 :
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "./img/ex.png"
                else:
                    half_fruit_path = "img/" + "h_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_fruits(key)
    if score<=20:
        FPS=10
    elif score<=30:
        FPS=11
    elif score<=40:
        FPS=12
    elif score<=50:
        FPS=13
    else:
        FPS=15
    pygame.display.update()
    clock.tick(FPS)
    # keys=pygame.key.get_pressed()
                         

pygame.quit()