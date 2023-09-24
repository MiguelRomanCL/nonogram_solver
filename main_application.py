import tkinter as tk
from input_hints import InputHints


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NonoGram - Main Menu")

        self.start_button = tk.Button(
            self, text="Start", command=self.launch_input_hints
        )
        self.start_button.pack(pady=20)

    def launch_input_hints(self):
        self.start_button.destroy()
        self.input_hints = InputHints(self)
