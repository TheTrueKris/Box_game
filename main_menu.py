import pygame
import sys

class MainMenu:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.FPS = 60
        self.options_menu = False
        self.volume = 50  # Placeholder for volume level
        self.back_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 75,  # Adjust the x-coordinate to center the button
            250,  # Set the y-coordinate for the back button
            150,  # Set the width of the back button
            50    # Set the height of the back button
        )
        
        # Load arrow images
        self.arrow_left_original = pygame.image.load("assets/arrow_left.png").convert_alpha()
        self.arrow_right_original = pygame.image.load("assets/arrow_right.png").convert_alpha()

        # Resize arrow images
        arrow_width, arrow_height = 40, 40  # Set the desired width and height for the arrows
        self.arrow_left = pygame.transform.scale(self.arrow_left_original, (arrow_width, arrow_height))
        self.arrow_right = pygame.transform.scale(self.arrow_right_original, (arrow_width, arrow_height))

        # Set the position of the arrow hitboxes
        self.arrow_rect_left = pygame.Rect(
            self.screen.get_width() // 2 - 125,  # Adjust x-coordinate for the left arrow
            190,  # Set y-coordinate for the left arrow
            arrow_width,
            arrow_height
        )
        self.arrow_rect_right = pygame.Rect(
            self.screen.get_width() // 2 + 100,  # Adjust x-coordinate for the right arrow
            190,  # Set y-coordinate for the right arrow
            arrow_width,
            arrow_height
        )

    def render(self):
        self.screen.fill((0, 0, 0))

        if not self.options_menu:
            title = self.font.render("Main Menu", True, "white")
            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

            play_option = self.font.render("Play Game", True, "white")
            self.screen.blit(play_option, (self.screen.get_width() // 2 - play_option.get_width() // 2, 200))

            options_option = self.font.render("Options", True, "white")
            self.screen.blit(options_option, (self.screen.get_width() // 2 - options_option.get_width() // 2, 250))

            quit_option = self.font.render("Quit", True, "white")
            self.screen.blit(quit_option, (self.screen.get_width() // 2 - quit_option.get_width() // 2, 300))
        else:
            self.render_options_menu()

        pygame.display.flip()

    def render_options_menu(self):
        title = self.font.render("Options", True, "white")
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        volume_label = self.font.render("Volume: {}".format(self.volume), True, "white")
        self.screen.blit(volume_label, (self.screen.get_width() // 2 - volume_label.get_width() // 2, 200))

        # Render arrow graphics
        self.screen.blit(self.arrow_left, self.arrow_rect_left)
        self.screen.blit(self.arrow_right, self.arrow_rect_right)

        back_option = self.font.render("Back", True, "white")
        self.screen.blit(back_option, (self.screen.get_width() // 2 - back_option.get_width() // 2, 250))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.options_menu:
                    if self.is_mouse_over(200, 250):  # Play Game button
                        return False, "Play Game"
                    elif self.is_mouse_over(250, 300):  # Options button
                        self.options_menu = True
                    elif self.is_mouse_over(300, 350):  # Quit button
                        return False, "Quit"
                else:
                    self.handle_options_menu_input()

        return True, None

    def handle_options_menu_input(self):
        if self.is_mouse_over_rect(self.back_button_rect):  # Back button
            self.options_menu = False
        elif self.is_mouse_over_rect(self.arrow_rect_left):  # Adjust volume down
            self.volume = max(0, self.volume - 5)
            self.sound_manager.set_volume(self.volume)
        elif self.is_mouse_over_rect(self.arrow_rect_right):  # Adjust volume up
            self.volume = min(100, self.volume + 5)
            self.sound_manager.set_volume(self.volume)

    def is_mouse_over_rect(self, rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return rect.collidepoint(mouse_x, mouse_y)

    def is_mouse_over(self, y_start, y_end):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            self.screen.get_width() // 2 - 150 <= mouse_x <= self.screen.get_width() // 2 + 150
            and y_start <= mouse_y <= y_end
        )

    def run(self):
        while True:
            self.render()
            exit_menu, selected_option = self.handle_input()

            if not exit_menu:
                return selected_option

            self.clock.tick(self.FPS)
