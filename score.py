import pygame
import time

class ScoreManager:
    def __init__(self, screen_width, screen_height):
        self.score = 0
        self.high_score = self.load_high_score()  # Load high score from file
        self.font = pygame.font.SysFont("timesnewroman", 36)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_food_time = None

    def increase_score(self, food_count):
        time_difference = 0
        
        if self.last_food_time is not None:
            time_difference = time.time() - self.last_food_time
        
        if time_difference < 0.5:
            increment = 1 + (food_count - 1) ** 2
        else:
            increment = 1 + (food_count - 1)
        
        self.score += increment
        self.last_food_time = time.time()

    def render_score(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, "white")
        screen.blit(score_text, (self.screen_width - score_text.get_width() - 10, 10))

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, "white")
        screen.blit(high_score_text, (10, 10))

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()  # Save high score to file

        self.score = 0
        self.last_food_time = None
        
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))