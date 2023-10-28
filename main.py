from game_manager import GameManager

def main():
    # Set the desired width and height
    width = 960
    height = 600

    # Create an instance of GameManager and run the game
    game_manager = GameManager(width, height)
    game_manager.run()

if __name__ == "__main__":
    main()