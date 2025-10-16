import pygame
import random
import os

# --- Initialize sound system ---
pygame.mixer.init()

# Path to sound folder (adjust if needed)
SOUND_DIR = os.path.join(os.path.dirname(__file__), "..", "sounds")

# Load sounds
paddle_hit_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "paddle_hit.wav"))
wall_bounce_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "wall_bounce.wav"))
score_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.wav"))


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

    def move(self, player=None, ai=None):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom edges
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            wall_bounce_sound.play()

        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            wall_bounce_sound.play()

        # Paddle collisions
        if player and self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            paddle_hit_sound.play()

        elif ai and self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            paddle_hit_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        score_sound.play()  # Play scoring sound when round resets

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
