import random
from engine import *


class Shield(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, shield_width, shield_height):
        super().__init__()

        self.shield_sprites = []
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "blueshield.png")), (shield_width, shield_height)))
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "purpleshield.png")), (shield_width, shield_height)))
        self.shield_sprites.append(pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "redshield.png")), (shield_width, shield_height)))

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

    def update(self, enemies, bullets, shields, character):
        self.rect.y -= BULLETS_VEL
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                enemy.colition = True
                for user_character in character:
                    user_character.score += enemy.score
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

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", picture_path)),
            (SPACE_WIDTH, SPACE_HEIGHT))

        if picture_path == "alien.png":
            self.score = 10
        if picture_path == "alien2.png":
            self.score = 5

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.colition = False
        self.explotion = 0

        self.max_enemy_bullets = 0
        self.enemy_bullets_probability = 0

    def destruction(self):
        if self.explotion <= len(self.explotion_sprites):
            self.image = self.explotion_sprites[int(self.explotion)]
        self.explotion += 0.1
        # EXPLOSION.play()

        if self.explotion > len(self.explotion_sprites):
            self.kill()

    def attack(self, enemies, enemy_bullets):

        if len(enemies) > 16:
            self.enemy_bullets_probability = 0.00001
            self.max_enemy_bullets = 1
        elif len(enemies) > 8:
            self.enemy_bullets_probability = 0.00002
            self.max_enemy_bullets = 2
        elif len(enemies) > 6:
            self.enemy_bullets_probability = 0.0001
            self.max_enemy_bullets = 3
        for enemy in enemies:
            if random.random() < self.enemy_bullets_probability and len(enemy_bullets) < self.max_enemy_bullets:
                new_alien_bullet = AlienBullet("laser.png", (enemy.rect.x + MAIN_WIDTH // 2 - 2), enemy.rect.y)
                enemy_bullets.add(new_alien_bullet)
                ENEMY_BULLET_SOUND.play()

    def update(self, enemies, enemy_bullets, shields, character, enemy_direction, enemy_vel):
        print(enemy_vel)
        if enemy_direction == "left":
            self.rect.x += enemy_vel

        elif enemy_direction == "right":
            self.rect.x -= enemy_vel

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
                n.health -= 5


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

        self.image = self.explotion_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        self.explotion = 0
        self.colition = False
        self.score = 0
        self.health = 4
        for n in range(self.health):
            new_live = PlayerLive("Space1.png", LIFE_X_POSITION[n], 30)
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
                    new_live = PlayerLive("Space1.png", LIFE_X_POSITION[n], 30)
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
    for user in character:
        score_text = SCORE_FONT.render(f"Score: {user.score}", True, WHITE)
        WIN.blit(score_text, (SCORE_X, SCORE_Y))
    # for bullet in bullets:
    #     pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def pause():
    pygame.display.update()
    pygame.time.delay(5000)


def show_level(level):
    level_text = LEVEL_FONT.render(f"Level: {level}", True, WHITE)
    WIN.blit(level_text, (250, 400))

    pygame.display.update()
    pygame.time.delay(5000)


def game_over():
    draw_text = GAMEOVER_FONT.render("Game Over", True, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)
