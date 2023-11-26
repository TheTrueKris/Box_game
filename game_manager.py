import pygame
from food import Foods
from collision import CollisionManager
from player import Player
from main_menu import MainMenu
from sound_manager import SoundManager
from score import ScoreManager
from ball import Ball
from barrier import Barrier

class GameManager:
    def __init__(self, width, height):
        pygame.init()
        # Get the screen dimensions
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        # Calculate the center position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        pygame.display.set_caption("A Box Game...")
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.topleft = (x, y)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.FPS = 60
        self.food_count = 0
        
        # Create an instance of SoundManager
        self.sound_manager = SoundManager()

        # Load background music and sound effects
        self.sound_manager.load_background_music("assets/background_music.mp3")
        self.sound_manager.load_sound_effect("eat_sound", "assets/eat_sound.mp3")
        
        # Creates an instance of MainMenu
        self.main_menu = MainMenu(self.screen, self.sound_manager)
        self.in_main_menu = True

        # Initializes the food manager and sets the amount of food to 5
        self.food_manager = Foods(width, height, food_amount=5)
        # Spawns food
        self.food_manager.spawn_food(eaten_food = [])

        # Creates the player instance
        self.player = Player(width, height)
        
        # Creates an instance of the score
        self.score_manager = ScoreManager(width, height)
        
        # Creates the ball instance
        self.ball = Ball(width, height, self.player, self.handle_game_over)
        
        # Create the barrier instance
        self.barrier = Barrier(width, height, self.player)
        
    def handle_game_over(self):
        # Restart the game
        self.player.reset_player(self.screen.get_width(), self.screen.get_height())
        self.ball.reset_ball()
        self.score_manager.reset_score()
        self.food_count = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.in_main_menu = not self.in_main_menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.barrier.activate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.barrier.deactivate()

    def update(self):
        # Moves and wraps the player
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.dt)
        self.player.wrap_around(self.screen)
        
        # Update the ball
        self.ball.move(self.dt)

        # Checks for collision between the player and food
        eaten_food = CollisionManager.check_collision(
            self.player.get_temp_rect(), self.food_manager.foods_list,
            self.screen.get_width(), self.screen.get_height()
        )
        if eaten_food:
            self.sound_manager.stop_sound_effect("eat_sound")
            self.sound_manager.play_sound_effect("eat_sound")
            # Respawn only the missing food
            self.food_manager.spawn_food(eaten_food)
            # Increment food count and update the score
            self.food_count += 1
            self.score_manager.increase_score(self.food_count)
            
        # Check for collision between the player and the ball
        if CollisionManager.is_collision(
            self.player.get_temp_rect(), self.ball.x, self.ball.y, self.ball.radius
        ):
            self.handle_game_over()
            
        # Updates the barrier
        self.barrier.dt = self.dt
        if self.barrier.is_active:
            self.barrier.update(self.ball)
            
        # Updates the display
        pygame.display.flip()

    def render(self):
        self.screen.fill("black")
        
        # Renders the food
        self.food_manager.render_food(self.screen)
        
        # Draw the player
        self.player.draw(self.screen)
        
        # Draw the ball
        self.ball.draw(self.screen)
        
        # Draw the barrier
        self.barrier.draw(self.screen)
        
        # Renders the score
        self.score_manager.render_score(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            
            if self.in_main_menu:
                selected_option = self.main_menu.run()
                if selected_option == "Play Game":
                    self.in_main_menu = False
                    # Plays background music when entering the game
                    self.sound_manager.play_background_music()
                    self.handle_game_over()
                    
                elif selected_option == "Quit":
                    pygame.quit()
                    return
            else:
                self.update()
                self.render()

                # Sets tick rate to 60
                self.dt = self.clock.tick(self.FPS) / 1000

        # Stop background music when quitting the game
        self.sound_manager.stop_background_music()
        # Quits pygame
        pygame.quit()
