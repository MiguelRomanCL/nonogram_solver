import tkinter as tk
from input_hints import (
    InputHints,
)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NonoGram - Welcome")

        # Creando el mensaje de bienvenida
        self.welcome_label = tk.Label(
            self, text="Welcome to NonoGram!", font=("Arial", 24), pady=20
        )
        self.welcome_label.pack(pady=20)

        # Ajustando el botón "Start"
        self.start_button = tk.Button(
            self, text="Start", command=self.launch_input_hints, font=("Arial", 16)
        )
        self.start_button.pack(pady=20)

    def launch_input_hints(self):
        self.welcome_label.destroy()
        self.start_button.destroy()
        self.input_hints = InputHints(
            self
        )  # Esta será la pantalla que crearemos a continuación
