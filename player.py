import pygame
import math
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.rect = pygame.Rect(screen.get_width() / 2 - 20, screen.get_height() / 2 - 20, 40, 40)
        self.speed = 300
        self.direction = (0, 0)
        self.projectiles = pygame.sprite.Group()

    def move(self, keys, dt):
        # Check for arrow key presses and update direction
        if keys[pygame.K_w]:
            self.direction = (0, -1)
        elif keys[pygame.K_s]:
            self.direction = (0, 1)
        elif keys[pygame.K_a]:
            self.direction = (-1, 0)
        elif keys[pygame.K_d]:
            self.direction = (1, 0)

        # Update the player's position based on direction and speed
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt

    def wrap_around(self, screen):
        if self.rect.x > screen.get_width():
            self.rect.x -= screen.get_width()
        elif self.rect.x < 0:
            self.rect.x += screen.get_width()

        if self.rect.y > screen.get_height():
            self.rect.y -= screen.get_height()
        elif self.rect.y < 0:
            self.rect.y += screen.get_height()

    def draw(self, screen):
        # Create a temporary rect to check if the player is partially off-screen
        temp_rect = self.get_temp_rect()

        # Draw the player on both sides if it's partially off-screen
        if self.rect.x < 0:
            pygame.draw.rect(screen, "white", temp_rect.move(screen.get_width(), 0))
        elif self.rect.x + self.rect.width > screen.get_width():
            pygame.draw.rect(screen, "white", temp_rect.move(-screen.get_width(), 0))

        if self.rect.y < 0:
            pygame.draw.rect(screen, "white", temp_rect.move(0, screen.get_height()))
        elif self.rect.y + self.rect.height > screen.get_height():
            pygame.draw.rect(screen, "white", temp_rect.move(0, -screen.get_height()))

        # Draw the original player rect if it's on-screen
        if self.rect.colliderect(pygame.Rect(0, 0, screen.get_width(), screen.get_height())):
            pygame.draw.rect(screen, "white", self.rect)

    def get_temp_rect(self):
        return self.rect.copy()

    def reset_player(self, screen_width, screen_height):
        self.rect = pygame.Rect(screen_width / 2 - 20, screen_height / 2 - 20, 40, 40)
        self.direction = (0, 0)  # Reset direction
        self.projectiles = pygame.sprite.Group()
        
    def attack(self, mouse_pos):
        # Calculate the position of the projectile based on the player's position
        player_center = (
            self.rect.centerx,
            self.rect.centery,
        )
        # Calculate the angle from player to mouse position
        angle = math.atan2(
            mouse_pos[1] - player_center[1],
            mouse_pos[0] - player_center[0],
        )

        # Calculate the initial position of the projectile based on player's center
        projectile_x = self.rect.centerx
        projectile_y = self.rect.centery

        # Create a projectile with the calculated angle and position
        projectile = Projectile(projectile_x, projectile_y, angle)
        self.projectiles.add(projectile)