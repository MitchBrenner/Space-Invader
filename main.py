import time

import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('low-angle-shot-mesmerizing-starry-sky.jpg')

# Background sound
# mixer.music.load('background.wav')
# mixer.music.player(-1)  # -1 plays on loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('portal.jpeg')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
# ready - you can't see the bullet
# fire - the bullet is currently moving
bulletImg = pygame.image.load('white-circle-emoji.png')
bulletImg = pygame.transform.scale(bulletImg, (16, 16))
bulletX = playerX
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"


def player(x, y):  # player function
    # blit means to draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 24, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    global num_of_enemies
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Score
score_value = 0
font = pygame.font.Font('retro.ttf', 48)

textX = 10
textY = 10


def show_score(x, y):
    # first you have to render text then you can blit it on the screen
    score = font.render("Score: " + str(score_value), True, (0, 175, 0))
    screen.blit(score, (x, y))


# Game over text
over_font = pygame.font.Font('retro.ttf', 128)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (200, 0, 0))
    screen.blit(over_text, (185, 200))


# Game Loop
running = True
while running:

    # change the background color
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:

            explosion_sound = mixer.Sound('mixkit-sea-mine-explosion-1184.wav')
            explosion_sound.set_volume(.5)
            explosion_sound.play(maxtime=1000)
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        # bullet_sound = mixer.Sound('lazer-reverb-13090.mp3')
        # bullet_sound.set_volume(.1)
        # bullet_sound.play(maxtime=500)
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # need to update screen
    pygame.display.update()
