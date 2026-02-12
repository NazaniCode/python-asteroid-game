import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        containers = getattr(type(self), "containers", ())
        super().__init__(*containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        r1 = self.radius
        r2 = other.radius
        distance = self.position.distance_to(other.position)
        if r1 + r2 >= distance:
            return True
        else:
            return False
