import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_SIZE = (50,50)
ENEMY_SIZE = (41,41)
BULLET_SIZE = (16,32)
ICON_SIZE = (32,32)
PLAYER_START_X = SCREEN_WIDTH // 2 - PLAYER_SIZE[0] // 2
PLAYER_START_Y = SCREEN_HEIGHT - PLAYER_SIZE[1] - 30
PLAYER_SPEED = 5

ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 3
ENEMY_SPEED_Y = 50
GAME_OVER_Y = PLAYER_START_Y - ENEMY_SIZE[1]
BULLET_SPEED_Y = 30
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
def load_image(path,size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img,size)


background = pygame.image.load("background_s.jpg").convert()
background = pygame.transform.smoothscale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Space Invader")
pygame.display.set_icon(load_image("ufo.png",ICON_SIZE))

player_image = load_image("player.png",PLAYER_SIZE)
player_X = PLAYER_START_X
player_Y = PLAYER_START_Y
player_X_change = 0 


num_enemies = 6
enemy_image = load_image("enemy.png",ENEMY_SIZE)
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemy_Y_change = []

for _ in range(num_enemies):
    enemy_X.append(random.randint(0,SCREEN_WIDTH - ENEMY_SIZE[0]))
    enemy_Y.append(random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX))
    enemy_X_change.append(ENEMY_SPEED_X)
    enemy_Y_change.append(ENEMY_SPEED_Y)


bullet_img = load_image("bullet.png",BULLET_SIZE)
bullet_x = 0
bullet_y = PLAYER_START_Y
bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 56)
game_over = False


def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(over_text, rect)

def player(x,y):
    screen.blit(player_image,(x,y))

def enemy(x,y):
    screen.blit(enemy_image,(x,y))

def fire_bullet(x,y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bullet_img,(x,y))

def is_collision(ex,ey,bx,by):
    enemy_rect = pygame.Rect(ex,ey,*ENEMY_SIZE)
    bullet_rect = pygame.Rect(bx,by,*BULLET_SIZE)
    return enemy_rect.colliderect(bullet_rect)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                player_X_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_X_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                # Center the bullet on the player
                bullet_x = player_X + PLAYER_SIZE[0] // 2 - BULLET_SIZE[0] // 2
                bullet_y = player_Y
                fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            player_X_change = 0

    # Player movement
    player_X += player_X_change
    player_X = max(0, min(player_X, SCREEN_WIDTH - PLAYER_SIZE[0]))

    # Enemy movement
    if not game_over:
        for i in range(num_enemies):
            if enemy_Y[i] > GAME_OVER_Y:
                game_over = True
                break

            enemy_X[i] += enemy_X_change[i]
            if enemy_X[i] <= 0:
                enemy_X_change[i] = ENEMY_SPEED_X
                enemy_Y[i] += enemy_Y_change[i]
            elif enemy_X[i] >= SCREEN_WIDTH - ENEMY_SIZE[0]:
                enemy_X_change[i] = -ENEMY_SPEED_X
                enemy_Y[i] += enemy_Y_change[i]

            if bullet_state == "fire" and is_collision(enemy_X[i], enemy_Y[i], bullet_x, bullet_y):
                bullet_y = player_Y
                bullet_state = "ready"
                score_value += 1
                enemy_X[i] = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE[0])
                enemy_Y[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

            enemy(enemy_X[i], enemy_Y[i])

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = player_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= BULLET_SPEED_Y

    player(player_X, player_Y)
    show_score(textX, textY)

    if game_over:
        game_over_text()

    pygame.display.update()

pygame.quit()                    

