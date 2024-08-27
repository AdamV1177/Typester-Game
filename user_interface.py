import tkinter as tk

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
        self.text_box = tk.Text(self, font=("Courier", 14, "normal"),
                                fg=CH_BLUE, bg=CH_BEIGE, width=50, height=8,
                                state='disabled', pady=5, padx=5, wrap='word')
        self.text_box.grid(row=1, column=0, columnspan=5, pady=7, padx=10)

        # Add an entry for the user to type into
        self.text_entry = tk.Entry(self, width=30, font=("Courier", 20, "bold"), bg=CH_BEIGE, fg=CH_BLUE)
        self.text_entry.grid(row=2, column=0, columnspan=5, pady=10)
