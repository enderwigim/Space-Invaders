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

MAIN_WIDTH, MAIN_HEIGHT = 80, 70
SPACE_WIDTH, SPACE_HEIGHT = 60, 62
MAIN_CHARACTER = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Space1.png")), (MAIN_WIDTH, MAIN_HEIGHT))
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

VEL = 5
BULLETS_VEL = 7
ENEMY_VEL = 2
ENEMY_DIRECTION = "left"
ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10
MAX_BULLETS = 1

FPS = 60

        # def explotion(self):
        #     pass
        #     # if self.current_sprite < len(self.explotion_sprites):
        #     #     self.alienimage = self.explotion_sprites[self.current_sprite]
        #     # else:
        #     #     pass
        #     # self.current_sprite += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (5, 15))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, enemies, bullets):
        self.rect.y -= BULLETS_VEL
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                enemy.colition = True
                for bullet in bullets:
                    bullet.kill()
            if self.rect.y < 0:
                for bullet in bullets:
                    bullet.kill()





class Alien(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.explotion_sprites = []
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion1.png")), (SPACE_WIDTH, SPACE_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion2.png")), (SPACE_WIDTH, SPACE_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion3.png")), (SPACE_WIDTH, SPACE_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion4.png")), (SPACE_WIDTH, SPACE_HEIGHT)))
        self.explotion = 0
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (SPACE_WIDTH, SPACE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.colition = False

    def destruction(self):
        if self.explotion <= len(self.explotion_sprites):
            self.image = self.explotion_sprites[int(self.explotion)]
        self.explotion += 0.1

        if self.explotion > len(self.explotion_sprites):
            self.kill()



    def update(self, enemies):
        global ENEMY_VEL, ENEMY_DIRECTION
        if ENEMY_DIRECTION == "left":
            self.rect.x += ENEMY_VEL
        elif ENEMY_DIRECTION == "right":
            self.rect.x -= ENEMY_VEL
        if self.colition:
            self.destruction()


def enemies_movement_handler(enemies):
    global ENEMY_VEL, ENEMY_DIRECTION
    for enemy in enemies:
        if enemy.rect.x > WIDTH - SPACE_WIDTH:
            ENEMY_DIRECTION = "right"
            for n in enemies:
                n.rect.y += 25
        if enemy.rect.x < 0:
            ENEMY_DIRECTION = "left"
            for n in enemies:
                n.rect.y += 25


def draw_window(character, enemies, bullets):
    WIN.blit(background, (0, 0))
    WIN.blit(MAIN_CHARACTER, (character.x, character.y))
    # for enemy in enemies:
    #     if not enemy.colition:
    #         WIN.blit(enemy.alienimage, (enemy.x, enemy.y))
    #     else:
    #         pass
    enemies.draw(WIN)
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def main_character_handler(key_pressed, character):
    if key_pressed[pygame.K_LEFT] and character.x > 0:  # Left
        character.x -= VEL
    if key_pressed[pygame.K_RIGHT] and character.x < WIDTH - character.width:  # Right
        character.x += VEL

def handle_bullets(bullets, enemies):
    for bullet in bullets:
        bullet.rect.y -= BULLETS_VEL
        for enemy in enemies:
            if bullet.colliderect(enemy) and not enemy.colition:
                bullets.remove(bullet)
                enemy.colition = True
                enemy.destruction()
                enemy.kill()


        if bullet.y < 0:
            bullets.remove(bullet)


def main():
    user_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    number = 10

    for alien in range(10):
        alien_num = random.randint(1, 2)
        if alien_num == 1:
            alien_sprite = "alien.png"
        else:
            alien_sprite = "alien2.png"
        new_alien = Alien(alien_sprite, (SPACE_WIDTH + (SPACE_WIDTH * alien)), (SPACE_HEIGHT - 10))
        enemies.add(new_alien)

    for alien in range(10):
        alien_num = random.randint(1, 2)
        if alien_num == 1:
            alien_sprite = "alien.png"
        else:
            alien_sprite = "alien2.png"
        new_alien = Alien(alien_sprite, (SPACE_WIDTH + (SPACE_WIDTH * alien)), (SPACE_HEIGHT - 10) * 2)
        enemies.add(new_alien)
    # for n in range(7):
    #     alientype = random.randint(1, 2)
    #     enemies.append(Enemy(number + ((MAIN_WIDTH + 5) * n), 10, alientype))
    # for n in range(7):
    #     alientype = random.randint(1, 2)
    #     enemies.append(Enemy(number + ((MAIN_WIDTH + 5) * n), 10 + MAIN_HEIGHT, alientype))
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
                    new_bullet = Bullet("laser.png", (character.x + MAIN_WIDTH // 2 - 2), character.y)
                    user_bullets.add(new_bullet)

                    # bullet = pygame.Rect(
                    #     (character.x + character.width // 2), character.y, 5, 15)
                    # user_bullets.append(bullet)
        key_pressed = pygame.key.get_pressed()
        main_character_handler(key_pressed, character)
        enemies_movement_handler(enemies)
        user_bullets.update(enemies, user_bullets)
        enemies.update(enemies)
        # handle_bullets(user_bullets, enemies)
        draw_window(character, enemies, user_bullets)


if __name__ == "__main__":
    main()