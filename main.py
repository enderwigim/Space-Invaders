from entities import *

LEVEL = 1
ENEMY_VEL = 1.25
MAX_ENEMY_BULLETS = 1
ENEMY_BULLETS_PROBABILITY = 0.00001
ENEMY_LINES = 3
ENEMY_DIRECTION = "left"


def get_everything_to_zero():
    global ENEMY_VEL, ENEMY_DIRECTION, MAX_ENEMY_BULLETS, ENEMY_BULLETS_PROBABILITY, ENEMY_LINES

    ENEMY_VEL = 1.25
    ENEMY_DIRECTION = "left"
    MAX_ENEMY_BULLETS = 1
    ENEMY_BULLETS_PROBABILITY = 0.00001


def level_up():
    global ENEMY_VEL, ENEMY_DIRECTION, MAX_ENEMY_BULLETS, ENEMY_LINES, LEVEL, ENEMY_BULLETS_PROBABILITY

    LEVEL += 1
    ENEMY_VEL += 0.05 * LEVEL
    MAX_ENEMY_BULLETS = int(MAX_ENEMY_BULLETS + 0.1)
    ENEMY_BULLETS_PROBABILITY += (0.00001 * LEVEL)


def enemies_movement_handler(enemies):
    global ENEMY_DIRECTION, ENEMY_VEL
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


def create_enemies():
    enemies = pygame.sprite.Group()

    for n in range(1, ENEMY_LINES + 1):
        for alien in range(8):
            if n == 1:
                alien_num = 1
            else:
                alien_num = random.randint(1, 2)
            if alien_num == 1:
                alien_sprite = "alien.png"
            else:
                alien_sprite = "alien2.png"
            new_alien = Alien(
                alien_sprite, (SPACE_WIDTH + (SPACE_WIDTH * alien)), (SPACE_HEIGHT + 30) * n)
            enemies.add(new_alien)
    return enemies


def sprites_set_up():
    user_bullets = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    character = pygame.sprite.GroupSingle()
    lives = pygame.sprite.Group()

    for shield in range(3):
        new_shield = Shield((SHIELD_POSITION[shield]), 600, SHIELD_WIDTH, SHIELD_HEIGHT)
        shields.add(new_shield)

    new_character = Player("Space1.png", 400, 700, lives)
    character.add(new_character)
    return user_bullets, shields, enemy_bullets, character, lives


user_bullets, shields, enemy_bullets, character, lives = sprites_set_up()
enemies = create_enemies()


def game():
    global enemies
    clock = pygame.time.Clock()
    draw_window(character, enemies, user_bullets, shields, enemy_bullets, lives)
    level_start = True
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

        if level_start:
            show_level(LEVEL)
            level_start = False
        key_pressed = pygame.key.get_pressed()
        character.update(key_pressed, character, enemy_bullets, enemies, lives)
        enemies_movement_handler(enemies)
        user_bullets.update(enemies, user_bullets, shields, character)
        shields.update()
        enemies.update(enemies, enemy_bullets, shields, character, ENEMY_DIRECTION, ENEMY_VEL)
        enemy_bullets.update(character, enemy_bullets, shields)
        draw_window(character, enemies, user_bullets, shields, enemy_bullets, lives)

        if len(enemies) == 0:
            get_everything_to_zero()
            level_up()
            enemies = create_enemies()
            game()


if __name__ == "__main__":
    sprites_set_up()
    game()
