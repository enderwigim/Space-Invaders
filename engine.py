import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

MAIN_WIDTH, MAIN_HEIGHT = 100, 100
SPACE_WIDTH, SPACE_HEIGHT = 60, 62
SHIELD_WIDTH, SHIELD_HEIGHT = 130, 60
SHIELD_POSITION = [136, 403, 670]
BULLET_WIDTH, BULLET_HEIGHT = 7, 20
LIFE_WIDTH, LIFE_HEIGHT = 40, 42
LIFE_X_POSITION = [-200, 50, 90, 130]
SCORE_X, SCORE_Y = 330, 10


pygame.font.init()
SCORE_FONT = pygame.font.SysFont("courier", 25)
GAMEOVER_FONT = pygame.font.SysFont('courier', 100)
LEVEL_FONT = pygame.font.SysFont('courier', 60)

pygame.mixer.init()
MAIN_BULLET_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "Laser Blaster.mp3"))
ENEMY_BULLET_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "Laser Enemy.mp3"))
# EXPLOSION = pygame.mixer.Sound(os.path.join("Assets/sounds", "Explosion.mp3"))

background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

VEL = 5
BULLETS_VEL = 7

ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10

MAX_BULLETS = 1


FPS = 60
