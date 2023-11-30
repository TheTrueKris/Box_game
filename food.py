import pygame
import random

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/food.png").convert_alpha()  # Load image
        self.rect = self.image.get_rect()

class Foods(pygame.sprite.Group):
    def __init__(self, initial_food_amount):
        super().__init__()
        self.initial_food_amount = initial_food_amount
        self.food_amount = initial_food_amount
        self.elapsed_time = 0


    def spawn_food(self, screen, dt, eaten_food):
        for food in eaten_food:
            self.remove(food)

        # Increase the food amount over time
        self.elapsed_time += dt
        if self.elapsed_time >= 5:  # Adjust the time threshold as needed
            self.food_amount += 1
            self.elapsed_time = 0

        while len(self.sprites()) < self.food_amount:
            food = Food()
            food.rect.x = random.randint(0, screen.get_width())
            food.rect.y = random.randint(0, screen.get_height())
            self.add(food)
            
            
    def reset_food(self):
        self.empty()
        self.food_amount = self.initial_food_amount
        self.elapsed_time = 0

    def render_food(self, screen):
        self.draw(screen)
