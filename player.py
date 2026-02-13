import sys
from logger import log_event
import pygame
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_INITIAL_LIVES,
    PLAYER_RADIUS,
    PLAYER_RESPAWN_DURATION,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.__is_respawning = False
        self.current_respawn_duration = 0
        self.current_respawn_direction = -1
        self.color = (255, 255, 255)
        self.is_invincible = False
        self.lives = PLAYER_INITIAL_LIVES

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        sped_up_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += sped_up_vector

    def shoot(self):
        if self.shot_cooldown_timer <= 0:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, 1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity *= PLAYER_SHOOT_SPEED
            self.shot_cooldown_timer = PLAYER_SHOT_COOLDOWN_SECONDS

    def die(self):
        if self.lives == 1:
            log_event("player_hit")
            print("Game over!")
            sys.exit()
        else:
            self.lives -= 1
            self.respawn()

    def respawn(self):
        if self.current_respawn_duration <= 0:
            self.__is_respawning = True
            self.is_invincible = True
            self.current_respawn_duration = PLAYER_RESPAWN_DURATION
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def play_respawn(self, dt):
        if self.color[0] <= 50:
            self.current_respawn_direction = 1
        if self.color[0] >= 255:
            self.current_respawn_direction = -1
        self.color = tuple(
            min(x + dt * self.current_respawn_direction * 1000, 255) for x in self.color
        )

    def finish_respawn(self):
        self.color = (255, 255, 255)
        self.is_invincible = False

    def update(self, dt):
        self.shot_cooldown_timer -= dt
        if self.__is_respawning:
            self.play_respawn(dt)
            self.current_respawn_duration -= dt
            if self.current_respawn_duration <= 0:
                self.__is_respawning = False
                self.finish_respawn()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_t]:
            self.respawn()
