import pygame
import random
import time
import math

class Ball:
    def __init__(self, screen_width, screen_height, player, on_game_over):
        self.radius = 15
        self.color = (255, 0, 0)  # Red
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.on_game_over = on_game_over
        self.reset_ball()

    def reset_ball(self):
        self.x = random.randint(self.radius, self.screen_width - self.radius * 2)
        self.y = random.randint(self.radius, self.screen_height - self.radius * 2)
        self.speed = 200  # Adjust the speed as needed
        self.direction = random.uniform(0, 2 * math.pi)  # Random initial direction
        self.last_collision_time = 0
        
        if time.time() - self.last_collision_time < 0.15:
            # Player has invulnerability for 0.2 seconds
            return

    def move(self, dt):
        # Update ball position based on direction and speed
        self.x += self.speed * dt * math.cos(self.direction)
        self.y += self.speed * dt * math.sin(self.direction)

        # Bounce back when the ball hits the screen edges
        if self.x - self.radius < 0 or self.x + self.radius > self.screen_width:
            self.direction = math.pi - self.direction
        if self.y - self.radius < 0 or self.y + self.radius > self.screen_height:
            self.direction = -self.direction

        # Increase speed over time
        self.speed += 1  # You can adjust the speed increment as needed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
