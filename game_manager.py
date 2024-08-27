import tkinter as tk
from tkinter import END


class Game:
    """
    Class taking care of the game functionality.
    - Adding new prompts to type with essential_generators package.
    """
    def __init__(self, frame, gen):
        self.frame = frame
        self.gen = gen
        self.generate_text()
        self.assign_command()

    def assign_command(self):
        """
        Assign the generate_text method to the Change prompt button, since I don't have
        a reference to the Game class in the MainApp class and can't do it there.
        """
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(command=self.generate_text)

    def generate_text(self):
        """
        Creates new prompt and places it into the textbox
        """
        # Create new prompt with Markov Generator and cut off to max 200 characters
        prompt = self.gen.gen_text()
        short_prompt = prompt[0:300]

        # Replace generated new line chars with normal spaces
        short_prompt = short_prompt.replace("\n", " ")

        # Find Text widget in the frame and add the new prompt
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Text):
                widget.configure(state='normal')
                widget.delete('1.0', END)
                widget.insert("1.0", short_prompt)
                widget.configure(state='disabled')
