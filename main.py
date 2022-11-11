import pygame
import os
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode(size=(WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

MAIN_WIDTH, MAIN_HEIGHT = 70, 60
SPACE_WIDTH, SPACE_HEIGHT = 120, 120
MAIN_CHARACTER = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Space1.png")), (SPACE_WIDTH, SPACE_HEIGHT))
ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "alien.png")), (MAIN_WIDTH, MAIN_HEIGHT))
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

VEL = 5
BULLETS_VEL = 7
ENEMY_VEL = 2
ENEMY_DIRECTION = 1
ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10
MAX_BULLETS = 1

FPS = 60


class Enemy(pygame.Rect):
    def __init__(self, x, y, alientype):
        super().__init__(x, y, MAIN_WIDTH, MAIN_HEIGHT)
        self.colition = False
        self.type = alientype
        self.explotion_sprites = []
        self.explotion_sprites.append(pygame.image.load(os.path.join("Assets", "explotion1.png")))
        self.explotion_sprites.append(pygame.image.load(os.path.join("Assets", "explotion2.png")))
        self.explotion_sprites.append(pygame.image.load(os.path.join("Assets", "explotion3.png")))
        self.current_sprite = 0
        if alientype == 1:
            self.alienimage = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "alien.png")),
                                                (MAIN_WIDTH, MAIN_HEIGHT))
            self.Score = 5
        if alientype == 2:
            self.alienimage = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "alien2.png")),
                                                (MAIN_WIDTH, MAIN_HEIGHT))

    def explotion(self):
        pass
        # if self.current_sprite < len(self.explotion_sprites):
        #     self.alienimage = self.explotion_sprites[self.current_sprite]
        # else:
        #     pass
        # self.current_sprite += 1





def draw_window(character, enemies, bullets):
    WIN.blit(background, (0, 0))
    WIN.blit(MAIN_CHARACTER, (character.x, character.y))
    for enemy in enemies:
        if not enemy.colition:
            WIN.blit(enemy.alienimage, (enemy.x, enemy.y))
        else:
            pass

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
        if WIDTH - MAIN_WIDTH > enemies[n].x > 0:
            enemies[n].x += (ENEMY_VEL * ENEMY_DIRECTION)

        if enemies[n].x <= 0:
            ENEMY_DIRECTION = 1
            ENEMY_VEL += 0.05
            for enemy in enemies:
                enemy.y += 10
                enemy.x += 10
            # enemies[n].x = enemies[1].x - MAIN_WIDTH

        elif enemies[n].x >= WIDTH - MAIN_WIDTH:
            ENEMY_DIRECTION = -1
            ENEMY_VEL += 0.05
            for enemy in enemies:
                enemy.y += 10
                enemy.x -= 10


def handle_bullets(bullets, enemies):
    for bullet in bullets:
        bullet.y -= BULLETS_VEL
        for enemy in enemies:
            if bullet.colliderect(enemy) and not enemy.colition:
                bullets.remove(bullet)
                enemy.explotion()
                enemy.colition = True
                # if enemy == enemies[1] and enemies[0].colition == False:
                #     enemies[1].colition = True
                # else:
                #     enemies.remove(enemy)
        if bullet.y < 0:
            bullets.remove(bullet)


def main():
    user_bullets = []
    enemies = []
    number = 10

    for n in range(7):
        alientype = random.randint(1, 2)
        enemies.append(Enemy(number + ((MAIN_WIDTH + 5) * n), 10, alientype))
    for n in range(7):
        alientype = random.randint(1, 2)
        enemies.append(Enemy(number + ((MAIN_WIDTH + 5) * n), 10 + MAIN_HEIGHT, alientype))
    character = pygame.Rect(250, 650, MAIN_WIDTH, MAIN_HEIGHT)
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
                        (character.x + character.width // 2 + 20), character.y, 5, 15)
                    user_bullets.append(bullet)
        key_pressed = pygame.key.get_pressed()
        main_character_handler(key_pressed, character)
        enemies_movement_handler(enemies)
        handle_bullets(user_bullets, enemies)
        draw_window(character, enemies, user_bullets)


if __name__ == "__main__":
    main()