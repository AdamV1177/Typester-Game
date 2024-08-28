import tkinter as tk
from tkinter import END
from user_interface import CH_BLUE
from pynput.keyboard import Key
import json
import datetime
from tkinter.messagebox import askyesno

# CONSTANTS
COUNTDOWN_LEN_S = 90


class Game:
    """
    Class taking care of the game functionality.
    - Adding new prompts to type with wonderwords package.
    - Handling keypresses and giving feedback to the user through text coloring.
    - Controlling the countdown
    - Starting/Ending rounds
    - Saving scores into scoreboard
    """
    def __init__(self, frame, gen, leaderboard):
        self.frame = frame
        self.gen = gen
        self.character_count = 0
        self.mistakes = 0
        self.leaderboard = leaderboard

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
            self.character_count += len(prompt_content)-1
            self.count_mistakes(entry_content, prompt_content)
            self.generate_text()

    def countdown(self, count=COUNTDOWN_LEN_S):
        """
        Function taking care of the countdown.
        Recursively called until countdown is at 0.
        """
        # If the countdown has just started, delete the current contents
        # of the textboxes and reset score.
        if count == COUNTDOWN_LEN_S:
            self.reset()
            self.start_button.configure(text="Stop Round", command=self.stop_round)

        # Add leading zero to single digits
        if count >= 10:
            self.countdown_label.configure(text=f"{count}")
        else:
            self.countdown_label.configure(text=f"0{count}")

        if count > 0:
            self.timer = self.frame.after(1000, self.countdown, count - 1)
        else:
            self.frame.after_cancel(self.timer)
            self.round_end()

    def round_end(self):
        """
        Function called when the countdown has run out.
        Shows the round results and leaderboard.
        """
        # Count the characters and mistakes in the last unfinished sentence
        self.character_count += len(self.input_box.get("1.0", END)) - 1
        self.count_mistakes(self.input_box.get("1.0", END).strip(), self.prompt_box.get("1.0", END).strip())

        # Save the results
        self.save_result()

        # Reset
        self.reset()

    def count_mistakes(self, entry, prompt):
        """
        Counts mistakes by comparing entry to prompt character by character.
        """
        for i in range(len(entry)):
            if entry[i] != prompt[i]:
                self.mistakes += 1

    def reset(self):
        """
        Resets the game to a blank slate with a new sentence.
        """
        self.generate_text()
        self.input_box.delete("1.0", END)
        self.character_count = 0
        self.mistakes = 0
        self.countdown_label.configure(text="90")
        self.start_button.configure(text='Start Timer', command=self.countdown)

    def stop_round(self):
        """
        Stop the current round and resets timer.
        Switches the button back to start.
        """
        self.reset()
        self.frame.after_cancel(self.timer)

    def save_result(self):

        # Count characters per minute and mistake ratio
        cpm = round(self.character_count/(COUNTDOWN_LEN_S/60), 1)

        if self.mistakes != 0:
            mistake_ratio = int(round(1 / (self.mistakes/self.character_count), 0))
        else:
            mistake_ratio = "N/A"

        # Ask user if they want to save the score
        response = askyesno("Save Score",
                            message=f"Your score:\n"
                            f"Characters per minute: {cpm}\n"
                            f"Mistakes: {self.mistakes}\n"
                            f"Mistake Ratio: 1 mistake in about every {mistake_ratio} characters.\n\n"
                            f"Do you want to save this score?")

        # If user wants to save score
        if response:

            # Read json with scores list
            try:
                with open('scoreboard.json') as json_file:
                    data = json.load(json_file)
                    scores_list = data['scores']

            # Create file if not found
            except FileNotFoundError:
                open("scoreboard.json", "x")
                scores_list = []

            # Create scores list if file exists but is empty and continue
            except json.decoder.JSONDecodeError:
                scores_list = []

            # Append new score to the list
            new_score = {
                "date": datetime.datetime.now().strftime("%d/%m/%Y"),
                "cpm": cpm,
                "mistakes": self.mistakes,
                "MR": mistake_ratio
            }
            scores_list.append(new_score)

            # Create dictionary to write into the json
            new_json = {
                "scores": scores_list
            }

            # Write new json into the scoreboards file
            with open("scoreboard.json", "w") as file:
                json.dump(new_json, file, indent=4)

            # Update the scoreboard in the leaderboard object (JSON only gets read when initialized)
            # After a new score is added, need to read the JSON again
            self.leaderboard.update_scoreboard()
