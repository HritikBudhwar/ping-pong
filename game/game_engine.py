import pygame
from .paddle import Paddle
from .ball import Ball
import sys

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # Default winning score
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball and handle collisions in one go
        self.ball.move(self.player, self.ai)

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Update AI paddle
        self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        # When someone reaches the winning score
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner = "Player" if self.player_score >= self.winning_score else "AI"

            # Prepare text surfaces
            font_large = pygame.font.SysFont("Arial", 60)
            font_small = pygame.font.SysFont("Arial", 40)

            winner_text = font_large.render(f"{winner} Wins!", True, (255, 255, 255))
            score_text = font_small.render(
                f"Final Score: {self.player_score} - {self.ai_score}",
                True,
                (200, 200, 200)
            )

            # Draw to screen
            screen.fill((0, 0, 0))
            screen.blit(winner_text, winner_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
            screen.blit(score_text, score_text.get_rect(center=(self.width // 2, self.height // 2 + 10)))
            pygame.display.flip()

            pygame.time.delay(2000)  # brief pause before replay menu
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        """Display replay options and wait for user input."""
        menu_font = pygame.font.SysFont("Arial", 36)
        small_font = pygame.font.SysFont("Arial", 28)

        while True:
            screen.fill((0, 0, 0))
            title = menu_font.render("Play Again?", True, (255, 255, 255))
            option1 = small_font.render("Press 3 for Best of 3", True, (200, 200, 200))
            option2 = small_font.render("Press 5 for Best of 5", True, (200, 200, 200))
            option3 = small_font.render("Press 7 for Best of 7", True, (200, 200, 200))
            option4 = small_font.render("Press ESC to Exit", True, (255, 100, 100))

            screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 100)))
            screen.blit(option1, option1.get_rect(center=(self.width // 2, self.height // 2 - 20)))
            screen.blit(option2, option2.get_rect(center=(self.width // 2, self.height // 2 + 30)))
            screen.blit(option3, option3.get_rect(center=(self.width // 2, self.height // 2 + 80)))
            screen.blit(option4, option4.get_rect(center=(self.width // 2, self.height // 2 + 150)))
            pygame.display.flip()

            # Wait for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_3:
                        self.start_new_game(3)
                        return
                    elif event.key == pygame.K_5:
                        self.start_new_game(5)
                        return
                    elif event.key == pygame.K_7:
                        self.start_new_game(7)
                        return

    def start_new_game(self, target_score):
        """Reset scores and ball for a new round."""
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = target_score
        self.ball.reset()
