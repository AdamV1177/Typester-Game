import tkinter as tk
from user_interface import MainApp
from game_manager import Game
from essential_generators import MarkovTextGenerator


def main():

    # Create Tk object and configure
    root = tk.Tk()
    root.title("Typester")
    root.resizable(False, False)

    # Create the main window UI
    main_window = MainApp(root)
    main_window.pack(expand=True)

    # Create text generator object
    gen = MarkovTextGenerator()

    # Create a new game in the main window
    game = Game(main_window, gen)

    root.mainloop()


if __name__ == "__main__":
    main()
