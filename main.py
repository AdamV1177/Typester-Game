import tkinter as tk
from user_interface import MainApp, Leaderboard
from game_manager import Game
from wonderwords import RandomSentence
from pynput import keyboard


def main():

    # Create Tk object and configure
    root = tk.Tk()
    root.title("Typester")
    root.resizable(False, False)

    # Create the main window UI and the leaderboard UI
    main_window = MainApp(root)
    leaderboard = Leaderboard(root)

    # Create text generator object
    gen = RandomSentence()

    # Create a new game in the main window
    game = Game(main_window, gen, leaderboard)

    # Create listener for keyboard input
    listener = keyboard.Listener(on_press=game.key_press)
    listener.start()

    root.mainloop()


if __name__ == "__main__":
    main()
