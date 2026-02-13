import pygame
from circleshape import CircleShape
from constants import PLAYER_INITIAL_LIVES, SCREEN_HEIGHT, SCREEN_WIDTH


class UI(CircleShape):
    def __init__(self, x, y, radius, player):
        super().__init__(10, 10, 30)
        self.score_position = (x, y)
        self.lives_position = (x, y + SCREEN_HEIGHT / 20)
        self.font = pygame.font.SysFont(None, SCREEN_WIDTH * SCREEN_HEIGHT // 30000)
        self.points = 0
        self.score_text = f"Score: {self.points}"
        self.lives_text = f"Lives: {player.lives}"
        self.player = player

    def draw(self, screen):
        self.score_text = f"Score: {self.points}"
        self.lives_text = f"Lives: {self.player.lives}"
        score_text_surface = self.font.render(self.score_text, True, "white")
        score_text_rect = score_text_surface.get_rect(center=self.score_position)
        screen.blit(score_text_surface, score_text_rect)

        lives_text_surface = self.font.render(self.lives_text, True, "white")
        lives_text_rect = lives_text_surface.get_rect(center=self.lives_position)
        screen.blit(lives_text_surface, lives_text_rect)
