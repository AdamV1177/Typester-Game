import tkinter as tk
from tkinter import END
from user_interface import CH_BLUE
from pynput.keyboard import Key

# CONSTANTS
COUNTDOWN_LEN_S = 60


class Game:
    """
    Class taking care of the game functionality.
    - Adding new prompts to type with wonderwords package.
    - Handling keypresses and giving feedback to the user through text coloring.
    """
    def __init__(self, frame, gen):
        self.frame = frame
        self.gen = gen

        # Find the widgets in the frame to assign
        text_widgets = []
        buttons = []
        labels = []
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Text):
                text_widgets.append(widget)
            elif isinstance(widget, tk.Button):
                buttons.append(widget)
            elif isinstance(widget, tk.Label):
                labels.append(widget)

        # Save the respective text widgets
        self.prompt_box = text_widgets[0]
        self.input_box = text_widgets[1]

        # Save the respective buttons
        self.change_prompt_button = buttons[0]
        self.start_button = buttons[1]

        # Save the label
        self.countdown_label = labels[1]

        self.generate_text()
        self.assign_commands()

        # Create variable for timer
        self.timer = ""

    def assign_commands(self):
        """
        Assign the methods to their respective buttons, since I don't have
        a reference to the Game class in the MainApp class and can't do it there.
        """
        self.change_prompt_button.configure(command=self.generate_text)
        self.start_button.configure(command=self.countdown)

    def generate_text(self):
        """
        Creates new prompt and places it into the textbox
        """
        # Create new sentence with wonder words
        prompt = self.gen.sentence()

        # Add text to only
        self.prompt_box.configure(state='normal')
        self.prompt_box.delete('1.0', END)
        self.prompt_box.insert("1.0", prompt)
        self.prompt_box.configure(state='disabled')

        # Clear input text box
        self.input_box.delete("1.0", END)

    def key_press(self, key):
        """
        Function called when a key on the keyboard is pressed.
        """
        # Get next word in the prompt
        prompt_content = self.prompt_box.get("1.0", END)

        # Get current content of the input text box
        entry_content = self.input_box.get("1.0", END)

        # Change deleted text back to blue if backspace is pressed
        if key == Key.backspace:
            for tag in self.prompt_box.tag_names():
                self.prompt_box.tag_delete(tag)

            self.prompt_box.tag_add(f"backtag", f"1.0", END)
            self.prompt_box.tag_config(f"backtag", foreground=CH_BLUE, font=("Courier", 20, "normal"))

        # Change color in the prompt box based on the length and correctness in the input box
        # tag_counter, to create unique tags
        tag_counter = 0
        for i in range(len(entry_content)-1):

            self.prompt_box.tag_add(f"start{tag_counter}", f"1.{i}", f"1.{i+1}")

            if prompt_content[i] == entry_content[i]:
                self.prompt_box.tag_config(f"start{tag_counter}", foreground="green", font=("Courier", 20, "bold"))
            else:
                self.prompt_box.tag_config(f"start{tag_counter}", foreground="red", font=("Courier", 20, "bold"))

            tag_counter += 1

        # Generate new sentence after the current one is finished
        if len(entry_content) == len(prompt_content):
            self.generate_text()

    def countdown(self, count=COUNTDOWN_LEN_S):
        if count >= 10:
            self.countdown_label.configure(text=f"{count}")
        else:
            self.countdown_label.configure(text=f"0{count}")

        if count > 0:
            self.timer = self.frame.after(1000, self.countdown, count - 1)
        else:
            self.frame.after_cancel(self.timer)
            # TODO: implement function to call after the countdown ends (display results of the game/round)
            print("Game end.")
