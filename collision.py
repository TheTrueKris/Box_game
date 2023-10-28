import pygame

class CollisionManager:
    @staticmethod
    def check_collision(player_rect, foods, screen_width, screen_height):
        eaten_food = []

        # Check for collision with the player's original position
        for food_rect in foods:
            if player_rect.colliderect(food_rect):
                eaten_food.append(food_rect)

        # Check for collision with the player's wrapped-around positions
        wrapped_player_rects = [
            player_rect.move(screen_width, 0),
            player_rect.move(-screen_width, 0),
            player_rect.move(0, screen_height),
            player_rect.move(0, -screen_height),
        ]

        for wrapped_rect in wrapped_player_rects:
            for food_rect in foods:
                if wrapped_rect.colliderect(food_rect):
                    eaten_food.append(food_rect)

        return eaten_food
    
    @staticmethod
    def is_collision(player_rect, x, y, radius):
        # Check for collision with the player's rect
        player_circle = pygame.draw.circle(
            pygame.Surface((player_rect.width, player_rect.height)),
            "white",
            (player_rect.width // 2, player_rect.height // 2),
            player_rect.width // 2
        )
        player_circle.x = player_rect.x
        player_circle.y = player_rect.y

        return player_circle.colliderect(x - radius, y - radius, radius * 2, radius * 2)