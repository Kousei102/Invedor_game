import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player setup
player_width, player_height = 50, 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 5

# Bullet setup
bullet_width, bullet_height = 5, 15
bullet_speed = -7
bullets = []

# Enemy setup
enemy_width, enemy_height = 50, 30
enemy_speed = 3
enemies = []
rows, cols = 5, 10
for row in range(rows):
    for col in range(cols):
        enemies.append(pygame.Rect(col * (enemy_width + 10) + 50, row * (enemy_height + 10) + 50, enemy_width, enemy_height))

# Game variables
running = True
clock = pygame.time.Clock()
score = 0

# Font setup
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Shooting bullets
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit number of bullets
            bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))

    # Update bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.x += enemy_speed

        # Reverse direction and move down
        if enemy.right >= WIDTH or enemy.left <= 0:
            enemy_speed *= -1
            for e in enemies:
                e.y += enemy_height
            break

        # Check for collisions with bullets
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break

        pygame.draw.rect(screen, GREEN, enemy)

    # Check for game over
    for enemy in enemies:
        if enemy.y + enemy_height >= player_y:
            draw_text("Game Over!", WIDTH // 2 - 100, HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    # Draw score
    draw_text(f"Score: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
