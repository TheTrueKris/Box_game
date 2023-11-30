import pygame
import random
import sys


class WindowPicker:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.sizes = [(800, 600), (960, 600), (1280, 720), (1920, 1080), None]
        self.selected_size = None
        
    
    def get_random_size(self):
        # Random size for the last button in the window picker
        random_width = random.randint(600, 1920)
        random_height = random.randint(400, 1080)
        return (random_width, random_height)
    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for idx, size in enumerate(self.sizes):
                        button_rect = pygame.Rect((self.screen.get_width() - 300) // 2, 50 + idx * 50, 300, 40)
                        if button_rect.collidepoint(x, y):
                            if size is None:
                                self.selected_size = self.get_random_size()
                            else:
                                self.selected_size = size
                            return

            self.render()

    def render(self):
        self.screen.fill((255, 255, 255))
        x_coordinate = (self.screen.get_width() - 300) // 2
        button_width = 300
        button_height = 40

        for idx, size in enumerate(self.sizes):
            button_rect = pygame.Rect(x_coordinate, 50 + idx * 50, button_width, button_height)
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)

            if size is None:
                text = self.font.render("?", True, (0, 0, 0))
            else:
                text = self.font.render(f"{size[0]} x {size[1]}", True, (0, 0, 0))
            self.screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

        pygame.display.flip()