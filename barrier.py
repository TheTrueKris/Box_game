import pygame
import math

class Barrier:
    def __init__(self, screen_width, screen_height, player):
        self.width = 10
        self.length = 60
        self.color = "white"
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.distance_from_player = 75  # Adjust the distance as needed
        self.is_active = False

    def update(self, ball):
        # Calculate the position of the barrier based on the player's position
        player_center = (
            self.player.rect.x + self.player.rect.width / 2,
            self.player.rect.y + self.player.rect.height / 2,
        )
        angle_to_mouse = math.atan2(
            pygame.mouse.get_pos()[1] - player_center[1],
            pygame.mouse.get_pos()[0] - player_center[0],
        )
        self.x = player_center[0] + self.distance_from_player * math.cos(angle_to_mouse)
        self.y = player_center[1] + self.distance_from_player * math.sin(angle_to_mouse)

        # Check for collision with the ball
        distance = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
        if distance <= self.length / 2 + ball.radius:
            # Reflect the ball's angle
            self.reflect_ball(ball, angle_to_mouse + math.pi)

    def reflect_ball(self, ball, incident_angle):
        # Calculate the normal vector of the barrier
        barrier_normal = pygame.Vector2(math.cos(incident_angle - math.pi / 2), math.sin(incident_angle - math.pi / 2))
        
        # Calculate the reflection angle using the normal vector
        reflection_angle = math.atan2(-barrier_normal.y, -barrier_normal.x)

        # Update the ball's direction without modifying the Ball class
        ball.direction = reflection_angle

    def draw(self, screen):
        if self.is_active:
            pygame.draw.rect(
                screen,
                self.color,
                (self.x - self.width / 2, self.y - self.length / 2, self.width, self.length),
            )

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
