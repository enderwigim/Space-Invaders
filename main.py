import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

MAIN_WIDTH, MAIN_HEIGHT = 70, 60
MAIN_CHARACTER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "spaceship_red.png")), (MAIN_WIDTH, MAIN_HEIGHT)), 180)
ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (MAIN_WIDTH, MAIN_HEIGHT))

VEL = 5
ENEMY_VEL = 2
ENEMY_DIRECTION = 1
ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10

FPS = 60


class Enemy:
    def __init__(self, x, y):
        self.colition = False
        self.enemy = pygame.Rect(x, y, MAIN_WIDTH, MAIN_HEIGHT)


def draw_window(character, enemies):
    WIN.fill(WHITE)
    WIN.blit(MAIN_CHARACTER, (character.x, character.y))
    for enemy in enemies:
        if not enemy.colition:
            WIN.blit(ENEMY, (enemy.enemy.x, enemy.enemy.y))
        else:
            pass
    pygame.display.update()


def main_character_handler(key_pressed, character):
    if key_pressed[pygame.K_LEFT] and character.x > 0:  # Left
        character.x -= VEL
    if key_pressed[pygame.K_RIGHT] and character.x < WIDTH - character.width:  # Right
        character.x += VEL


def enemies_movement_handler(enemies):
    global ENEMY_VEL, ENEMY_DIRECTION

    for n in range(0, len(enemies)):
        if enemies[-1].enemy.x < WIDTH - MAIN_WIDTH and enemies[0].enemy.x > 0:
            enemies[n].enemy.x += (ENEMY_VEL * ENEMY_DIRECTION)

        if enemies[0].enemy.x <= 0:
            ENEMY_DIRECTION = 1
            ENEMY_VEL += 0.05
            for enemy in enemies:
                enemy.enemy.y += 10
                enemy.enemy.x += 10
            enemies[0].enemy.x = enemies[1].enemy.x - MAIN_WIDTH

        elif enemies[-1].enemy.x >= WIDTH - MAIN_WIDTH:
            ENEMY_DIRECTION = -1
            ENEMY_VEL += 0.05
            for enemy in enemies:
                enemy.enemy.y += 10
                enemy.enemy.x -= 10


def main():
    bullets = []
    enemies = []
    number = 10
    for n in range(9):
        enemies.append(Enemy(number + (MAIN_WIDTH * n), 10))
    for n in range(9):
        enemies.append(Enemy(number + (MAIN_WIDTH * n), 10 + MAIN_HEIGHT))

    character = pygame.Rect(250, 700, MAIN_WIDTH, MAIN_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key_pressed = pygame.key.get_pressed()
        main_character_handler(key_pressed, character)
        enemies_movement_handler(enemies)
        draw_window(character, enemies)


if __name__ == "__main__":
    main()