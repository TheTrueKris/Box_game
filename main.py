import pygame
from game_manager import GameManager

def main(width, height):
    # Create an instance of GameManager and run the game
    game_manager = GameManager(width, height)
    game_manager.run()

def width_height_picker():
    pygame.init()

    # Define available window sizes
    sizes = [(800, 600), (960, 600), (1280, 720), (1920, 1080)]

    # Set up pygame window
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Window Size Picker")

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for idx, size in enumerate(sizes):
                    button_rect = pygame.Rect(50, 50 + idx * 50, 300, 40)
                    if button_rect.collidepoint(x, y):
                        width, height = size
                        main(width, height)

        screen.fill((255, 255, 255))

        # Draw buttons for each size
        for idx, size in enumerate(sizes):
            button_rect = pygame.Rect(50, 50 + idx * 50, 300, 40)
            pygame.draw.rect(screen, (200, 200, 200), button_rect)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

            text = font.render(f"{size[0]} x {size[1]}", True, (0, 0, 0))
            screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

        pygame.display.flip()

if __name__ == "__main__":
    width_height_picker()
