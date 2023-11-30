import pygame
import math
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
        self.screen = pygame.display.set_mode((width, height))
        self.screen_rect = self.screen.get_rect()
        self.screencopy = None
        self.screen_rect.topleft = (x, y)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.FPS = 60
        self.food_count = 0
        self.is_game_over = False
        
        self.ball_spawn_timer = 0
        self.ball_spawn_threshold = 5  # Time threshold for ball spawns in seconds
        
        # Load the in-game background image
        self.background = pygame.image.load("assets/ingame_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

        
        # Create an instance of SoundManager
        self.sound_manager = SoundManager()

        # Load background music and sound effects
        self.sound_manager.load_background_music("assets/background_music.mp3")
        self.sound_manager.load_sound_effect("eat_sound", "assets/eat_sound.mp3")
        
        # Creates an instance of MainMenu
        self.main_menu = MainMenu(self.screen, self.sound_manager)
        self.in_main_menu = True

        # Initializes the food manager and sets the amount of food to 5
        self.food_manager = Foods(initial_food_amount = 1)
        # Spawns food
        self.food_manager.spawn_food(self.screen, self.dt, eaten_food=[])

        # Creates the player instance
        self.player = Player(width, height)
        
        # Creates an instance of the score
        self.score_manager = ScoreManager(width, height)
        
        # Creates the ball instance
        self.ball = Ball(self.player, self.handle_game_over)
        self.balls = []
        
        # Create the barrier instance
        self.barrier = Barrier(self.player)
        
        # Starts the game
        self.handle_game_over()
        
    def handle_game_over(self):
        if self.is_game_over == False:
            # Clear existing balls
            self.balls = [self.ball]
            
            # Restart the game
            self.player.reset_player(self.screen.get_width(), self.screen.get_height())
            self.ball.reset_ball(self.screen)
            self.score_manager.reset_score()
            self.food_count = 0
            self.food_manager.reset_food()
            self.food_manager.spawn_food(self.screen, self.dt, eaten_food = [])
            self.ball_spawn_timer = 0 
            
        else:
            # Show game over screen
            self.game_over()
            
    def spawn_new_ball(self):
        # Remove dead balls from the list
        self.balls = [ball for ball in self.balls if ball.is_alive]

        new_ball = Ball(self.player, self.handle_game_over)
        # Check if the new ball overlaps with the player
        while pygame.sprite.spritecollide(new_ball, pygame.sprite.Group(self.player), False):
            new_ball.reset_ball(self.screen)  # Reposition the ball

        self.balls.append(new_ball)
        self.ball_spawn_timer = 0  # Reset the ball spawn timer

        
    def game_over(self):
        game_over_font = pygame.font.Font(None, 74)
        instruction_font = pygame.font.Font(None, 50)
        text = game_over_font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        text2 = instruction_font.render("Press Escape to return", True, (255, 0, 0))
        text_rect2 = text.get_rect(center=(self.screen.get_width() / 2.1, self.screen.get_height() / 1.5))

        while self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_game_over = False
                        for ball in self.balls:
                            ball.reset_ball(self.screen)  # Reset the ball after game over

                        self.handle_game_over()
                        return
            
            self.screen.blit(text, text_rect)
            self.screen.blit(text2, text_rect2)

            pygame.display.flip()
            self.clock.tick(self.FPS)
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.in_main_menu = not self.in_main_menu 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    self.player.attack(mouse_pos)
                if event.button == 3:  # Right mouse button
                    self.barrier.activate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Right mouse button
                    self.barrier.deactivate()
                
                    

    def update(self):
        # Moves and wraps the player
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.dt)
        self.player.wrap_around(self.screen)
        
        # Update the ball spawn timer
        self.ball_spawn_timer += self.dt
        
        # Check if it's time to spawn a new ball
        if self.ball_spawn_timer >= self.ball_spawn_threshold:
            self.spawn_new_ball()  # Spawn a new ball
        
        # Update the ball
        self.balls = [ball for ball in self.balls if ball.is_alive]  # Remove dead balls
        for ball in self.balls:
            ball.move(self.dt, self.screen)
            # Draw the HP bar for the ball
            ball.draw_hp_bar(self.screen)

        # Checks for collision between the player and food
        eaten_food = CollisionManager.check_collision(
            self.player.get_temp_rect(), self.food_manager.sprites(),
            self.screen.get_width(), self.screen.get_height()
        )
        if eaten_food:
            self.sound_manager.stop_sound_effect("eat_sound")
            self.sound_manager.play_sound_effect("eat_sound")
            # Increment food count and update the score
            self.food_count += 1
            self.score_manager.increase_score(self.food_count)
            
        self.food_manager.spawn_food(self.screen, self.dt, eaten_food)
            
        # Check for collision between the player and the balls
        ball_group = pygame.sprite.Group(self.balls)
        if pygame.sprite.spritecollide(self.player, ball_group, True):
            self.is_game_over = True
            self.handle_game_over()
        
        # Update projectiles
        for projectile in self.player.projectiles:
            projectile.move(self.dt)

        # Check for collision between projectiles and the ball
        for ball in ball_group:
            projectile_hit_list = pygame.sprite.spritecollide(ball, self.player.projectiles, True)
            for projectile in projectile_hit_list:
                # Handle projectile-ball collision (you can modify this logic)
                ball.take_damage(25)
                self.player.projectiles.remove(projectile)
                break
            
        # Updates the barrier
        self.barrier.dt = self.dt
        if self.barrier.is_active:
            for ball in self.balls:
                self.barrier.update(ball)
        
        # Updates the display
        pygame.display.flip()

    def render(self):
        # Draw the in-game background
        self.screen.blit(self.background, (0, 0))
        
        # Renders the food
        self.food_manager.render_food(self.screen)
        
        # Draw the player
        self.player.draw(self.screen)
        
        # Draw the ball
        for ball in self.balls:
            ball.draw(self.screen)
        
        # Draw the projectiles
        for projectile in self.player.projectiles:
            projectile.draw(self.screen)
        
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
                    
                elif selected_option == "Quit":
                    pygame.quit()
                    return
                
            else:
                self.update()
                self.render()
                
                if self.screencopy != (self.screen.get_width(), self.screen.get_height()):
                    self.screencopy = (self.screen.get_width(), self.screen.get_height())
                    # Restarts the game
                    self.handle_game_over()
                    self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

                # Sets tick rate to 60
                self.dt = self.clock.tick(self.FPS) / 1000

        # Stop background music when quitting the game
        self.sound_manager.stop_background_music()
        # Quits pygame
        pygame.quit()
