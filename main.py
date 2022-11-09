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
BULLETS_VEL = 7
ENEMY_VEL = 2
ENEMY_DIRECTION = 1
ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10
MAX_BULLETS = 1

FPS = 60


class Enemy:
    def __init__(self, x, y):
        self.colition = False
        self.enemy = pygame.Rect(x, y, MAIN_WIDTH, MAIN_HEIGHT)


def draw_window(character, enemies, bullets):
    WIN.fill(WHITE)
    WIN.blit(MAIN_CHARACTER, (character.x, character.y))
    for enemy in enemies:
        if not enemy.colition:
            WIN.blit(ENEMY, (enemy.enemy.x, enemy.enemy.y))
        else:
            continue
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
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


def handle_bullets(bullets, enemies):
    for bullet in bullets:
        bullet.y -= BULLETS_VEL
        for enemy in enemies:
            if bullet.colliderect(enemy.enemy) and not enemy.colition:
                bullets.remove(bullet)
                enemy.colition = True
        if bullet.y < 0:
            bullets.remove(bullet)


def main():
    user_bullets = []
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and len(user_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        (character.x + character.width // 2), character.y, 5, 10)
                    user_bullets.append(bullet)
        key_pressed = pygame.key.get_pressed()
        main_character_handler(key_pressed, character)
        enemies_movement_handler(enemies)
        handle_bullets(user_bullets, enemies)
        draw_window(character, enemies, user_bullets)


if __name__ == "__main__":
    main()