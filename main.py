import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 500, 800
WIN = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

MAIN_WIDTH, MAIN_HEIGHT = 70, 60
MAIN_CHARACTER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "spaceship_red.png")), (MAIN_WIDTH, MAIN_HEIGHT)), 180)
ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (MAIN_WIDTH, MAIN_HEIGHT))

VEL = 5
ENEMY_VEL = 3

FPS = 60


def draw_window(character, enemies):
    WIN.fill(WHITE)
    WIN.blit(MAIN_CHARACTER, (character.x, character.y))
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))
    pygame.display.update()


def main_character_handler(key_pressed, character):
    if key_pressed[pygame.K_LEFT] and character.x > 0:  # Left
        character.x -= VEL
    if key_pressed[pygame.K_RIGHT] and character.x < WIDTH - character.width:  # Right
        character.x += VEL


def enemies_movement_handler(enemies):
    global ENEMY_VEL
    if (MAIN_WIDTH * -1) < enemies[0].x < WIDTH:
        enemies[0].x += ENEMY_VEL
    if enemies[0].x < (MAIN_WIDTH * -1) or enemies[0].x > WIDTH:
        ENEMY_VEL = ENEMY_VEL * -1
        enemies[0].y += MAIN_WIDTH
        enemies[0].x += ENEMY_VEL
    for n in range(1, len(enemies)):
        if enemies[n].y == enemies[n - 1].y:
            enemies[n].x = enemies[n - 1].x - MAIN_HEIGHT
        else:
            if (MAIN_WIDTH * -1) < enemies[n].x < WIDTH + MAIN_HEIGHT:
                enemies[n].x += (ENEMY_VEL * -1)
            else:
                enemies[n].y = enemies[n - 1].y
            #     enemies[n].y = enemies[n - 1].y


def main():
    enemies = []
    for n in range(2):
        enemies.append(pygame.Rect(1, 10, MAIN_WIDTH, MAIN_HEIGHT))
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