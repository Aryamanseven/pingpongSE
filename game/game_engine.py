import pygame
from .paddle import Paddle
from .ball import Ball

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
        self.font = pygame.font.SysFont("Arial", 30)
        self.win_score = 5  # default win score

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Dynamic win check based on selected best-of
        if self.player_score >= self.win_score or self.ai_score >= self.win_score:
            self.show_game_over()

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

    def show_game_over(self):
        winner = "Player" if self.player_score > self.ai_score else "AI"
        screen = pygame.display.get_surface()
        font_big = pygame.font.SysFont("Arial", 50)
        text = font_big.render(f"{winner} Wins!", True, WHITE)
        screen.fill((0, 0, 0))
        screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - 100))

        small_font = pygame.font.SysFont("Arial", 30)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, opt in enumerate(options):
            line = small_font.render(opt, True, WHITE)
            screen.blit(line, (self.width//2 - line.get_width()//2, self.height//2 + i*40))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                        best_of = int(event.unicode)
                        self.win_score = (best_of // 2) + 1  # calculate dynamic win score
                        self.player_score = 0
                        self.ai_score = 0
                        self.ball.reset()
                        waiting = False
