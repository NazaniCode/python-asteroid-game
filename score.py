import pygame
from circleshape import CircleShape


class Score(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(10, 10, 30)
        self.score_position = (x, y)
        self.font = pygame.font.SysFont(None, 50)
        self.points = 0
        self.score_text = f"Score: {self.points}"

    def draw(self, screen):
        self.score_text = f"Score: {self.points}"
        text_surface = self.font.render(self.score_text, True, "white")
        text_rect = text_surface.get_rect(center=self.score_position)
        screen.blit(text_surface, text_rect)
