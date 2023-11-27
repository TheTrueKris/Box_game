import pygame
import random
import time
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, player, on_game_over):
        super().__init__()
        self.radius = 15
        self.color = (255, 0, 0)  # Red
        self.player = player
        self.x = player.rect.centerx
        self.y = player.rect.centery
        self.on_game_over = on_game_over
        self.max_hp = 100
        self.hp = self.max_hp
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def reset_ball(self, screen):
        self.screen = screen
        self.x = random.randint(self.radius * 2, screen.get_width() - self.radius * 2)
        self.y = random.randint(self.radius * 2, screen.get_height() - self.radius * 2)
        self.speed = 200  # Adjust the speed as needed
        self.direction = random.uniform(0, 2 * math.pi)  # Random initial direction
        self.last_collision_time = 0
        self.hp = self.max_hp
        
        if time.time() - self.last_collision_time < 0.15:
            # Player has invulnerability for 0.2 seconds
            return

    def move(self, dt, screen):
        # Update ball position based on direction and speed
        self.x += self.speed * dt * math.cos(self.direction)
        self.y += self.speed * dt * math.sin(self.direction)
        self.rect.center = (self.x, self.y)

        # Bounce back when the ball hits the screen edges
        if self.x - self.radius < 0 or self.x + self.radius > screen.get_width():
            self.direction = math.pi -self.direction
        if self.y - self.radius < 0 or self.y + self.radius > screen.get_height():
            self.direction = -self.direction
            
        # If ball is gone, teleport him back
        if self.x - self.radius < -50 or self.x + self.radius > screen.get_width() + 50:
            self.x = random.randint(self.radius * 2, screen.get_width() - self.radius * 2)
            self.y = random.randint(self.radius * 2, screen.get_height() - self.radius * 2)
        if self.y - self.radius < -50 or self.y + self.radius > screen.get_height() + 50:
            self.x = random.randint(self.radius * 2, screen.get_width() - self.radius * 2)
            self.y = random.randint(self.radius * 2, screen.get_height() - self.radius * 2)

        # Increase speed over time
        self.speed += 1  # You can adjust the speed increment as needed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.reset_ball(self.screen)
        
    def draw_hp_bar(self, screen):
        hp_bar_width = int(self.rect.width * (self.hp / self.max_hp))
        hp_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 10, hp_bar_width, 5)
        pygame.draw.rect(screen, (0, 255, 0), hp_bar_rect)