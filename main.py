import pygame

import os
import random
import time

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

pygame.font.init()
GAMEOVER_FONT = pygame.font.SysFont('comicsans', 100)

pygame.mixer.init()
MAIN_BULLET_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "Laser Blaster.mp3"))
ENEMY_BULLET_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "Laser Enemy.mp3"))
# EXPLOSION = pygame.mixer.Sound(os.path.join("Assets/sounds", "Explosion.mp3"))

background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

VEL = 5
BULLETS_VEL = 7
ENEMY_VEL = 1.25
ENEMY_DIRECTION = "left"
ENEMY_POSITION_X = 0
ENEMY_POSITION_Y = 10
MAX_ENEMY_BULLETS = 1
ENEMY_BULLETS_PROBABILITY = 0.00001

MAX_BULLETS = 1


FPS = 60


class Shield(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.shield_sprites = []
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "blueshield.png")), (SHIELD_WIDTH, SHIELD_HEIGHT)))
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "purpleshield.png")), (SHIELD_WIDTH, SHIELD_HEIGHT)))
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "redshield.png")), (SHIELD_WIDTH, SHIELD_HEIGHT)))

        self.image = self.shield_sprites[0]
        self.health = 25

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self):
        if self.health > 16:
            self.image = self.shield_sprites[0]
        elif self.health > 8:
            self.image = self.shield_sprites[1]
        elif self.health > 0:
            self.image = self.shield_sprites[2]
        else:
            self.kill()


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (BULLET_WIDTH, BULLET_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, enemies, bullets, shields):
        self.rect.y -= BULLETS_VEL
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                enemy.colition = True
                self.kill()
        if self.rect.y < 0:
            self.kill()
        for shield in shields:
            if self.rect.colliderect(shield):
                shield.health -= 1
                self.kill()


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
        # EXPLOSION.play()

        if self.explotion > len(self.explotion_sprites):
            self.kill()

    def attack(self, enemies, enemy_bullets):
        global MAX_ENEMY_BULLETS, ENEMY_BULLETS_PROBABILITY
        if len(enemies) > 16:
            MAX_ENEMY_BULLETS = 1
        elif len(enemies) > 8:
            ENEMY_BULLETS_PROBABILITY = 0.0001
            MAX_ENEMY_BULLETS = 2
        elif len(enemies) > 4:
            ENEMY_BULLETS_PROBABILITY = 0.001
            MAX_ENEMY_BULLETS = 3
        for enemy in enemies:
            if random.random() < ENEMY_BULLETS_PROBABILITY and len(enemy_bullets) < MAX_ENEMY_BULLETS:
                new_alien_bullet = AlienBullet("laser.png", (enemy.rect.x + MAIN_WIDTH // 2 - 2), enemy.rect.y)
                enemy_bullets.add(new_alien_bullet)
                ENEMY_BULLET_SOUND.play()

    def update(self, enemies, enemy_bullets, shields, character):
        global ENEMY_VEL, ENEMY_DIRECTION
        if ENEMY_DIRECTION == "left":
            self.rect.x += ENEMY_VEL

        elif ENEMY_DIRECTION == "right":
            self.rect.x -= ENEMY_VEL

        if self.colition:
            self.destruction()
        self.attack(enemies, enemy_bullets)
        for shield in shields:
            if self.rect.colliderect(shield):
                self.colition = True
                shield.health -= 5
        for n in character:
            if self.rect.colliderect(n):
                self.colition = True
                n.health -=5


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (BULLET_WIDTH, BULLET_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, character, bullets, shields):
        self.rect.y += BULLETS_VEL
        for n in character:
            if self.rect.colliderect(n):
                self.kill()
                n.health -= 1
                n.colition = True
        if self.rect.y > (800 - BULLET_HEIGHT):
            self.kill()
        for shield in shields:
            if self.rect.colliderect(shield):
                shield.health -= 1
                self.kill()


def enemies_movement_handler(enemies):
    global ENEMY_VEL, ENEMY_DIRECTION
    for enemy in enemies:
        if enemy.rect.x > WIDTH - SPACE_WIDTH:
            ENEMY_DIRECTION = "right"
            for n in enemies:
                n.rect.y += 10
            ENEMY_VEL += 0.05
        if enemy.rect.x < 0:
            ENEMY_DIRECTION = "left"
            for n in enemies:
                n.rect.y += 10
            ENEMY_VEL += 0.05

class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, lives):
        super().__init__()

        self.explotion_sprites = []
        self.explotion_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (MAIN_WIDTH, MAIN_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion1.png")), (MAIN_WIDTH, MAIN_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion2.png")), (MAIN_WIDTH, MAIN_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion3.png")), (MAIN_WIDTH, MAIN_HEIGHT)))
        self.explotion_sprites.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "explotion4.png")), (MAIN_WIDTH, MAIN_HEIGHT)))


        self.explotion = 0
        self.image = self.explotion_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.colition = False

        self.health = 4
        for n in range(self.health):
            new_live = PlayerLive("Space1.png", LIFE_X_POSITION[n], 760)
            lives.add(new_live)

    def destruction(self, lives):
        if self.explotion <= len(self.explotion_sprites):
            self.image = self.explotion_sprites[int(self.explotion)]
        self.explotion += 0.1
        # EXPLOSION.play()
        if self.explotion > len(self.explotion_sprites):
            if self.health > 0:
                pause()
                for live in lives:
                    live.kill()
                for n in range(self.health):
                    print(n)
                    new_live = PlayerLive("Space1.png", LIFE_X_POSITION[n], 760)
                    lives.add(new_live)
                self.explotion = 0
                self.colition = False
                self.image = self.explotion_sprites[0]
            else:
                for live in lives:
                    live.kill()
                pause()
                self.kill()
                game_over()



    def update(self, key_pressed, character, enemy_bullets, enemies, lives):
        if key_pressed[pygame.K_LEFT] and self.rect.x > 0:  # Left
            self.rect.x -= VEL
        if key_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH - MAIN_WIDTH:  # Right
            self.rect.x += VEL
        if self.colition:
            self.destruction(lives)

class PlayerLive(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (LIFE_WIDTH, LIFE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


def draw_window(character, enemies, bullets, shields, enemy_bullets, lives):
    WIN.blit(background, (0, 0))

    character.draw(WIN)
    enemies.draw(WIN)
    bullets.draw(WIN)
    shields.draw(WIN)
    enemy_bullets.draw(WIN)
    lives.draw(WIN)
    # for bullet in bullets:
    #     pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def pause():
    pygame.display.update()
    pygame.time.delay(5000)


def game_over():
    draw_text = GAMEOVER_FONT.render("Game Over", True, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    user_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    character = pygame.sprite.GroupSingle()
    lives = pygame.sprite.Group()

    for alien in range(8):
        alien_num = 1
        if alien_num == 1:
            alien_sprite = "alien.png"
        else:
            alien_sprite = "alien2.png"
        new_alien = Alien(alien_sprite, (SPACE_WIDTH + ((SPACE_WIDTH + 10) * alien)), (SPACE_HEIGHT - 15))
        enemies.add(new_alien)

    for alien in range(8):
        alien_num = random.randint(1, 2)
        if alien_num == 1:
            alien_sprite = "alien.png"
        else:
            alien_sprite = "alien2.png"
        new_alien = Alien(alien_sprite, (SPACE_WIDTH + ((SPACE_WIDTH + 10) * alien)), (SPACE_HEIGHT - 10) * 2)
        enemies.add(new_alien)

    for alien in range(8):
        alien_num = 2
        if alien_num == 1:
            alien_sprite = "alien.png"
        else:
            alien_sprite = "alien2.png"
        new_alien = Alien(alien_sprite, (SPACE_WIDTH + ((SPACE_WIDTH + 10) * alien)), (SPACE_HEIGHT - 10) * 3)
        enemies.add(new_alien)

    for shield in range(3):
        new_shield = Shield((SHIELD_POSITION[shield]), 600)
        shields.add(new_shield)

    new_character = Player("Space1.png", 400, 700, lives)
    character.add(new_character)



    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and len(user_bullets) < MAX_BULLETS:
                    for n in character:
                        new_bullet = PlayerBullet("laser.png", (n.rect.x + MAIN_WIDTH // 2 - 3), n.rect.y)
                        user_bullets.add(new_bullet)
                        MAIN_BULLET_SOUND.play()

        key_pressed = pygame.key.get_pressed()
        character.update(key_pressed, character, enemy_bullets, enemies, lives)
        enemies_movement_handler(enemies)
        user_bullets.update(enemies, user_bullets, shields)
        shields.update()
        enemies.update(enemies, enemy_bullets, shields, character)
        enemy_bullets.update(character, enemy_bullets, shields)
        draw_window(character, enemies, user_bullets, shields, enemy_bullets, lives)



if __name__ == "__main__":
    main()