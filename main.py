import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1200, 980
GRAVITY = 0.6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GROUND_Y = HEIGHT - 50
TRAIL_LENGTH = 50
PROJECTILE_RADIUS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulator (SAM1)")

catapult_pos = pygame.Vector2(WIDTH // 2, GROUND_Y)
projectile_pos = pygame.Vector2(catapult_pos)
target_pos = pygame.Vector2(WIDTH - 100, GROUND_Y - 20)

angle = 45
power = 50
projectile_velocity = pygame.Vector2(0, 0)
launched = False
score = 0
attempts = 10
trail_positions = []

font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def reset_shot():
    global launched, projectile_pos, projectile_velocity, trail_positions
    launched = False
    projectile_pos = pygame.Vector2(catapult_pos)
    projectile_velocity = pygame.Vector2(0, 0)
    trail_positions = []


clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 5)
    pygame.draw.circle(screen, WHITE, (int(catapult_pos.x), int(catapult_pos.y)), 20)

    if not launched:
        prediction_pos = pygame.Vector2(projectile_pos)
        rad = math.radians(angle)
        pred_vel = pygame.Vector2(math.cos(rad) * power, -math.sin(rad) * power)
        for i in range(1, 100):
            pred_vel.y += GRAVITY
            prediction_pos += pred_vel
            if prediction_pos.y + PROJECTILE_RADIUS >= GROUND_Y:
                break
            if i % 5 == 0:
                dot_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(dot_surface, (255, 255, 255, 128), (3, 3), 3)
                screen.blit(dot_surface, (int(prediction_pos.x) - 3, int(prediction_pos.y) - 3))


    if not launched:
        indicator_length = 50
        end_pos = pygame.Vector2(
            catapult_pos.x + math.cos(math.radians(angle)) * indicator_length,
            catapult_pos.y - math.sin(math.radians(angle)) * indicator_length
        )
        pygame.draw.line(screen, GREEN, catapult_pos, end_pos, 3)

        meter_rect = pygame.Rect(catapult_pos.x + 30, catapult_pos.y - 20, 10, 40)
        pygame.draw.rect(screen, WHITE, meter_rect, 1)
        fill_height = int(40 * (power / 50))
        pygame.draw.rect(screen, GREEN,
                         (meter_rect.left + 1, meter_rect.bottom - fill_height,
                          meter_rect.width - 1, fill_height))

    pygame.draw.circle(screen, RED, (int(projectile_pos.x), int(projectile_pos.y)), PROJECTILE_RADIUS)
    pygame.draw.rect(screen, GREEN, (target_pos.x - 25, target_pos.y - 25, 50, 50))

    space_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True

    keys = pygame.key.get_pressed()
    if not launched and attempts > 0:
        if keys[pygame.K_LEFT] and angle < 180:
            angle += 0.5
        if keys[pygame.K_RIGHT] and angle > 0:
            angle -= 0.5
        if keys[pygame.K_DOWN] and power > 5:
            power -= 0.5
        if keys[pygame.K_UP] and power < 50:
            power += 0.5

        if space_pressed:
            launched = True
            rad = math.radians(angle)
            projectile_velocity.x = math.cos(rad) * power
            projectile_velocity.y = -math.sin(rad) * power
            trail_positions = []

    if launched:
        projectile_velocity.y += GRAVITY
        projectile_pos += projectile_velocity

        if projectile_pos.y + PROJECTILE_RADIUS >= GROUND_Y:
            attempts -= 1
            reset_shot()

        target_rect = pygame.Rect(target_pos.x - 20, target_pos.y - 20, 50, 50)
        if target_rect.collidepoint(projectile_pos):
            score += 100
            target_pos = pygame.Vector2(random.randint(WIDTH // 2, WIDTH - 100), GROUND_Y - 20)
            reset_shot()
    else:
        if len(trail_positions) == 0 or projectile_pos.distance_to(trail_positions[-1]) > 5:
            trail_positions.append(pygame.Vector2(projectile_pos))
            if len(trail_positions) > TRAIL_LENGTH:
                trail_positions.pop(0)

    draw_text(f"Angle: {angle}°", WHITE, 10, 10)
    draw_text(f"Power: {power}", WHITE, 10, 50)
    draw_text(f"Score: {score}", WHITE, 10, 90)
    draw_text(f"Attempts left: {attempts}", WHITE, 10, 130)

    if attempts <= 0:
        draw_text("GAME OVER! Press R to restart", RED, WIDTH // 2 - 150, HEIGHT // 2)
        if keys[pygame.K_r]:
            score = 0
            attempts = 10
            target_pos = pygame.Vector2(random.randint(WIDTH // 2, WIDTH - 100), GROUND_Y - 20)
            reset_shot()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
