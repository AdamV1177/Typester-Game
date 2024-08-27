import tkinter as tk


class Game:
    """
    Class taking care of the game functionality.
    - Adding new prompts to type with essential_generators package.
    """
    def __init__(self, frame, gen):
        self.frame = frame
        self.gen = gen
        self.generate_text()

    def generate_text(self):
        """
        Creates new prompt and places it into the textbox
        """
        # Create new prompt with Markov Generator and cut off to max 200 characters
        prompt = self.gen.gen_text()
        prompt = prompt[0:300]

        # Replace generated new line chars with normal spaces
        prompt = prompt.replace("\n", " ")
        print(prompt)

        # Find Text widget in the frame and add the new prompt
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Text):
                widget.configure(state='normal')
                widget.insert("1.0", prompt)
                widget.configure(state='disabled')
