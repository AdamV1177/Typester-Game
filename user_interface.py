import tkinter as tk
import json
import operator

# CONSTANTS
# Colors from ColorHunt
CH_BLUE = "#102C57"
CH_BROWN = "#DAC0A3"
CH_WHITE = "#FEFAF6"
CH_BEIGE = "#EADBC8"


class MainApp(tk.Frame):
    """
    A tkinter frame containing the main application window.
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(bg=CH_BROWN)

        # Add welcome title
        self.welcome_label = tk.Label(self, text="Welcome to Typester!",
                                      fg=CH_BLUE, bg=CH_BROWN,
                                      font=("Courier", 20, "bold"))
        self.welcome_label.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        # Add the main text box for the to-be-typed text
        self.text_box = tk.Text(self, font=("Courier", 20, "normal"),
                                fg=CH_BLUE, bg=CH_BEIGE, width=50, height=3,
                                state='disabled', pady=5, padx=5, wrap='word')
        self.text_box.grid(row=1, column=0, columnspan=5, pady=7, padx=10)

        # Add a textbox for the user to type into
        self.text_entry = tk.Text(self, width=50, font=("Courier", 15, "bold"),
                                  bg=CH_WHITE, fg=CH_BLUE, height=2, wrap='word',
                                  )
        self.text_entry.grid(row=2, column=0, columnspan=4, pady=10)

        # Add button to change the text prompt
        self.change_prompt_button = tk.Button(self, fg=CH_BLUE, bg=CH_BEIGE, text="Change Prompt", highlightthickness=0)
        self.change_prompt_button.grid(row=3, column=1, pady=5)

        # Add timer label
        self.timer_label = tk.Label(self, fg=CH_BLUE, bg=CH_BROWN, text="90", font=("Arial", 40, "bold"))
        self.timer_label.grid(row=2, column=4)

        # Add start button
        self.start_button = tk.Button(self, fg=CH_BEIGE, bg=CH_BLUE, text="Start Timer", highlightthickness=0)
        self.start_button.grid(row=3, column=2, pady=5)

        # Add leaderboard button
        self.leaderboard_button = tk.Button(self, fg=CH_BLUE, bg=CH_BEIGE,
                                            text="Show Leaderboard", highlightthickness=0,
                                            command=self.show_leaderboard)
        self.leaderboard_button.grid(row=3, column=0, pady=5)

        self.pack(expand=True)

    def show_leaderboard(self):
        """
        Shows the leaderboard frame and hides the current main game frame.
        """

        # Remove self (main game frame)
        self.pack_forget()

        # Show leaderboard frame
        leaderboard_frame = self.parent.winfo_children()[1]
        leaderboard_frame.pack()


class Leaderboard(tk.Frame):
    """
    A tkinter frame to show the leaderboards in
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(bg=CH_BROWN)

        # Add welcome title
        self.title = tk.Label(self, text="Leaderboards TOP 10",
                              fg=CH_BLUE, bg=CH_BROWN,
                              font=("Courier", 20, "bold"))
        self.title.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        # Add label with scores
        self.scores = tk.Label(self, text="No scores yet.",
                               fg=CH_BLUE, bg=CH_BROWN,
                               font=("Courier", 15, "bold"))
        self.scores.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        self.update_scoreboard()

        # Add button to return to game
        self.back_button = tk.Button(self, fg=CH_BLUE, bg=CH_BEIGE,
                                     text="Back To Game", highlightthickness=0,
                                     command=self.show_game)
        self.back_button.grid(row=2, column=1, pady=5)

    def show_game(self):
        """
        Shows the game frame and hides the current leaderboard frame.
        """

        # Remove self (leaderboard frame)
        self.pack_forget()

        # Show game frame
        game_frame = self.parent.winfo_children()[0]
        game_frame.pack()

    def update_scoreboard(self):
        """
        Updates the text in the leaderboard frame.
        """
        # Open the json file with scores
        scores_list = []
        try:
            with open("scoreboard.json", "r") as json_file:
                data = json.load(json_file)
                scores_list = data['scores']
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

        # Create string with scores
        scores_string = "No scores yet."
        if scores_list:
            # Sort the list by CPM
            scores_list.sort(key=operator.itemgetter('cpm'), reverse=True)

            scores_string = ""
            rank = 1

            # Get only top ten from list
            top_10 = scores_list[0:10]
            for score_dict in top_10:
                scores_string = scores_string + f"{rank}. {score_dict['cpm']} cpm | {score_dict['MR']} MR\n"
                rank += 1

        self.scores.configure(text=scores_string)
