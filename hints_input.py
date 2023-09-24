import tkinter as tk
from nonogram_solver import NonoGramBoard


class InputHints(tk.Frame):
    def __init__(self, parent, number_of_rows, number_of_columns):
        super().__init__(parent)
        self.parent = parent

        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.row_hints = []
        self.col_hints = []

        self.label = tk.Label(
            self, text="Enter the hints for each row and column", font=("Arial", 16)
        )
        self.label.pack(pady=20)

        self.entry_label = tk.Label(self, text="Row 1:")
        self.entry_label.pack(pady=5)

        self.hint_entry = tk.Entry(self)
        self.hint_entry.pack(pady=5)

        self.add_button = tk.Button(self, text="Add", command=self.add_hint)
        self.add_button.pack(pady=20)

        self.pack(pady=100)

    def add_hint(self):
        hint = list(map(int, self.hint_entry.get().split(",")))
        if len(self.row_hints) < self.number_of_rows:
            self.row_hints.append(hint)
            next_label = f"Row {len(self.row_hints) + 1}:"
        else:
            self.col_hints.append(hint)
            next_label = f"Column {len(self.col_hints) + 1}:"

        if len(self.col_hints) == self.number_of_columns:
            self.confirm_hints()
            return

        self.entry_label.config(text=next_label)
        self.hint_entry.delete(0, tk.END)

    def confirm_hints(self):
        # Import NonoGramGUI here, right before we use it
        from interfaz import NonoGramGUI

        self.destroy_children()
        nonogram = NonoGramBoard(self.row_hints, self.col_hints)
        NonoGramGUI(self.parent, nonogram)

    def destroy_children(self):
        for child in self.winfo_children():
            child.destroy()
