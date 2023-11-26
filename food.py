import pygame
import random

pygame.init()

class Foods():
    def __init__(self, screen_width, screen_height, food_amount):
        self.food_amount = food_amount
        self.foods_list = []
        self.screen_width = screen_width
        self.screen_height = screen_height

    def spawn_food(self, eaten_food):
        for food_rect in eaten_food:
            self.foods_list.remove(food_rect)

        # Generate and add new food items to reach the desired amount
        while len(self.foods_list) < self.food_amount:
            food_x = random.randint(0, self.screen_width)
            food_y = random.randint(0, self.screen_height)
            food_rect = pygame.Rect(food_x, food_y, 10, 10)
            self.foods_list.append(food_rect)


    def render_food(self, screen):
        for food_rect in self.foods_list:
            pygame.draw.rect(screen, "white", food_rect)
