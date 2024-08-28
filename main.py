import tkinter as tk
from user_interface import MainApp
from game_manager import Game
from wonderwords import RandomSentence
from pynput import keyboard


def main():

    # Create Tk object and configure
    root = tk.Tk()
    root.title("Typester")
    root.resizable(False, False)

    # Create the main window UI
    main_window = MainApp(root)
    main_window.pack(expand=True)

    # Create text generator object
    gen = RandomSentence()

    # Create a new game in the main window
    game = Game(main_window, gen)

    # Create listener for keyboard input
    listener = keyboard.Listener(on_press=game.key_press)
    listener.start()

    root.mainloop()


if __name__ == "__main__":
    main()
