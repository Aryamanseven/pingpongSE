import pygame
import random

# Initialize mixer safely before loading sounds
pygame.mixer.init()

# Load sounds (make sure these files exist in the correct folder)
try:
    paddle_sound = pygame.mixer.Sound("game/paddle_hit.mp3")
    wall_sound = pygame.mixer.Sound("game/wall_bounce.mp3")
    score_sound = pygame.mixer.Sound("game/score.mp3")
except pygame.error:
    print("⚠️ Warning: Sound files not found or unsupported format. Sounds will be skipped.")
    paddle_sound = wall_sound = score_sound = None


class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if wall_sound:
                wall_sound.play(maxtime=2000)  # limit playback to 2 seconds

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        # Player paddle collision
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x = abs(self.velocity_x)
            if paddle_sound:
                paddle_sound.play(maxtime=2000)  # limit playback to 2 seconds

        # AI paddle collision
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x = -abs(self.velocity_x)
            if paddle_sound:
                paddle_sound.play(maxtime=2000)  # limit playback to 2 seconds

    def reset(self):
        # Reset ball to center
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if score_sound:
            score_sound.play(maxtime=2000)  # limit playback to 2 seconds

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
