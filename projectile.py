import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.width = 10
        self.length = 30
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Green
        self.speed = 500  # Adjust the speed as needed
        self.direction = direction
        self.projectile_image = pygame.image.load("assets/Projectile.png").convert_alpha()
        self.projectile_image = pygame.transform.scale(self.projectile_image, (self.width, self.length))
        # Update the rotation angle based on the mouse position
        self.rotation_angle = math.degrees(self.direction)
        self.projectile_image = pygame.transform.rotate(self.projectile_image, -self.rotation_angle)
        self.rect = self.projectile_image.get_rect(center=(self.x, self.y))

    def move(self, dt):
        # Update projectile position based on direction and speed
        self.x += self.speed * dt * math.cos(self.direction)
        self.y += self.speed * dt * math.sin(self.direction)
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Draw the rotated barrier image onto the screen
        screen.blit(self.projectile_image, self.rect.topleft)
