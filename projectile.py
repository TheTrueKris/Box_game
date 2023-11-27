import pygame
import math

class Projectile:
    def __init__(self, x, y, direction):
        self.radius = 5
        self.color = (0, 255, 0)  # Green
        self.x = x
        self.y = y
        self.speed = 500  # Adjust the speed as needed
        self.direction = direction

    def move(self, dt):
        # Update projectile position based on direction and speed
        self.x += self.speed * dt * math.cos(self.direction)
        self.y += self.speed * dt * math.sin(self.direction)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
