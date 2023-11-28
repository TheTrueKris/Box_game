from game_manager import GameManager

def main(width, height):
    # Create an instance of GameManager and run the game
    game_manager = GameManager(width, height)
    game_manager.run()

if __name__ == "__main__":
    main(960, 600)