# importing the pygame module along with some other modules
import pygame
import random
import math
from pygame import mixer

# initialising the pygame module
pygame.init()

# for creating the Game screen
game_screen = pygame.display.set_mode((800, 600))
game_state = "running"

# setting the name and icon of the display
pygame.display.set_caption("Space Wars")  # setting the title of the game
icon = pygame.image.load('images\\ufo.png')  # loading the icon
pygame.display.set_icon(icon)  # setting the icon for the display

# for player
playerImg = pygame.image.load('images\SpaceShip.png')
playerX = 400
playerY = 500
playerXchange = 0
playerYchange = 0

# for Enemies(six in total)
enemyImg = []
enemyImg.append(pygame.image.load('images\enemy1.png'))
enemyImg.append(pygame.image.load('images\enemy2.png'))
enemyImg.append(pygame.image.load('images\enemy3.png'))
enemyImg.append(pygame.image.load('images\enemy4.png'))
enemyImg.append(pygame.image.load('images\enemy5.png'))
enemyImg.append(pygame.image.load('images\enemy6.png'))
enemyX = []
enemyY = []

# assigning randon values to the enemies to appear on the screen
for i in range(6):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 350))

# changing x and y position of the enemies
enemyXchange = [0.5 for i in range(6)]
enemyYchange = [64 for i in range(6)]

# for bullet pair
bulletImg = pygame.image.load('images\\bulletpair.png')
# bullet will start from the player's place
bulletX = playerX
bulletY = playerY
bulletXchange = 0
bulletYchange = 0
# initially the state of the bullet is reloading means it is not fired
bullet_state = "reloading"


# fire bullet funciton
def fire_bullet(fx, fy):
    global bullet_state  # declaring it global will make it accesible to other funcitons
    bulletX = fx
    bullet_state = "running"
    # by giving the appropriate parameters to the blit function of the game_screen object, we place the image onto the screeen
    game_screen.blit(bulletImg, (bulletX, fy))


# Collision detection function
def are_colliding(x1, y1, x2, y2):  # coordinate of enemy(x1, y1) and bullet object(x2, y2)
    if math.sqrt(math.pow((x2 - (x1 + 15)), 2) + math.pow((y2 - (y1 + 15)), 2)) <= 25:  # checking for first bulletpair
        return True
    elif math.sqrt(math.pow(((x2 + 50) - (x1 + 15)), 2) + math.pow((y2 - (y1 + 15)),
                                                                   2)) <= 25:  # checking for the second bullet
        return True
    else:
        return False


# Background Image
Galaxy = pygame.image.load("images\galaxy.png")

# Background music
mixer.music.load('audio\\backgroundmusic.mp3')
mixer.music.play(-1)


# creating the player on the screen
def player(px, py):
    game_screen.blit(playerImg, (px, py))


# creating the enemy
def enemy(number, ex, ey):
    game_screen.blit(enemyImg[number], (ex, ey))


def game_over():
    global game_over_message
    for i in range(6):
        enemyY[i] = 1000
        enemyXchange[i] = 0
        enemyYchange[i] = 0

    game_over_font = pygame.font.Font("freesansbold.ttf", 64)  # freesansbold is freely available in pygame module
    game_over_message = game_over_font.render(" || GAME OVER ||", True, (240, 240, 240))  # render will render the text onto the screen with game_over_font
    game_screen.blit(game_over_message, (150, 250))


# Calculating game score
global game_score
game_score = 0


# score board function to tell the score
def score_board():
    score_font = pygame.font.Font("freesansbold.ttf", 30)
    score = score_font.render("Score: " + str(game_score), True, (255, 255, 255))
    game_screen.blit(score, (0, 0))


# this is the main game loop
while game_state == "running":
    # setting the background image
    game_screen.blit(Galaxy, (0, 0))
    for event in pygame.event.get():  # checking the every event happening during execution of the screen
        if event.type == pygame.QUIT:  # if the event type is quitting the game then we make the state of game stop
            game_state = "stop"
        if event.type == pygame.KEYDOWN:
            playerXchange = 0
            if event.key == pygame.K_LEFT:
                # moving left side
                playerXchange = -1

            if event.key == pygame.K_RIGHT:
                # moving right
                playerXchange = 1

            if event.key == pygame.K_SPACE:
                if bullet_state == "reloading":
                    bullet_sound = mixer.Sound('audio\shooting.wav')
                    bullet_sound.play()  # background sound for the music
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bulletYchange = -0.7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    # to display the player onto the screen continuosly
    playerX += playerXchange
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    player(playerX, playerY)

    # to display all the enemies onto the screen

    for i in range(6):
        if enemyX[i] <= 0:
            enemyXchange[i] = 0.5
            enemyY[i] += enemyYchange[i]
            # if any enemy reaches at the spaceship place then the game is over
            if enemyY[i] >= 450:
                game_over()
                break
        if enemyX[i] >= 736:
            enemyXchange[i] = -0.5
            enemyY[i] += enemyYchange[i]
            # if any enemy reaches at the spaceship place then the game is over
            if enemyY[i] >= 450:
                game_over()
                game_screen.blit(game_over_message, (150, 250))
                break
        enemyX[i] += enemyXchange[i]
        enemy(i, enemyX[i], enemyY[i])

    # checking whether the bullet has collided with the enemy
    bulletY += bulletYchange
    collide = False
    for i in range(6):
        collide = are_colliding(enemyX[i], enemyY[i], bulletX, bulletY)
        if collide:
            # collision sound upon collision
            collision_sound = mixer.Sound('audio\explosion.wav')
            collision_sound.play()
            game_score += 1
            bulletYchange = 0  # No change in the bullet along y axis now
            bulletY = playerY  # setting the initial posion of the bullet
            bullet_state = "reloading"  # setting the state to reloading
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(200, 350)
    if bulletY <= 0:  # at the end of the screen bullet will stop and reload
        bulletYchange = 0
        bulletY = playerY
        bullet_state = "reloading"
    if bullet_state == "running":
        fire_bullet(bulletX, bulletY)  # first bullet
        fire_bullet(bulletX + 50, bulletY)  # second bullet

    # showing the score board at every iteration
    score_board()
    # always update the disply after performing task
    pygame.display.update()
