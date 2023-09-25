import tkinter as tk
from input_hints import (
    InputHints,
)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NonoGram - Welcome")

        # Creating the welcome message
        self.welcome_label = tk.Label(
            self, text="Welcome to NonoGram!", font=("Arial", 24), pady=20
        )
        self.welcome_label.pack(pady=20)

        # Setting up the "Start" button
        self.start_button = tk.Button(
            self, text="Start", command=self.launch_input_hints, font=("Arial", 16)
        )
        self.start_button.pack(pady=20)

    def launch_input_hints(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.input_hints = InputHints(self)

    def show_welcome_screen(self):
        """Display the welcome screen with the Start button."""
        self.welcome_label = tk.Label(
            self, text="Welcome to NonoGram!", font=("Arial", 24), pady=20
        )
        self.welcome_label.pack(pady=20)

        self.start_button = tk.Button(
            self, text="Start", command=self.launch_input_hints, font=("Arial", 16)
        )
        self.start_button.pack(pady=20)
