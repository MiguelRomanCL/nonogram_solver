import tkinter as tk
from tkinter import messagebox
from nonogram_gui import NonoGramGUI
from nonogram_solver import NonoGramBoard


class InputHints:
    def __init__(self, parent):
        self.parent = parent

        self.row_label = tk.Label(self.parent, text="Number of Rows:")
        self.row_label.pack(pady=5)

        self.row_entry = tk.Entry(self.parent)
        self.row_entry.pack(pady=5)

        self.column_label = tk.Label(self.parent, text="Number of Columns:")
        self.column_label.pack(pady=5)

        self.column_entry = tk.Entry(self.parent)
        self.column_entry.pack(pady=5)

        self.submit_button = tk.Button(
            self.parent, text="Submit", command=self.get_hints
        )
        self.submit_button.pack(pady=20)

    def get_hints(self):
        try:
            number_of_rows = int(self.row_entry.get())
            number_of_columns = int(self.column_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter valid integers for rows and columns."
            )
            return

        self.row_label.destroy()
        self.row_entry.destroy()
        self.column_label.destroy()
        self.column_entry.destroy()
        self.submit_button.destroy()

        self.hint_labels = []
        self.row_hints_entries = []
        self.column_hints_entries = []

        for i in range(number_of_rows):
            label = tk.Label(self.parent, text=f"Row {i+1} Hints:")
            label.grid(row=i, column=0, padx=10, pady=5)
            self.hint_labels.append(label)

            entry = tk.Entry(self.parent)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.row_hints_entries.append(entry)

        for j in range(number_of_columns):
            label = tk.Label(self.parent, text=f"Column {j+1} Hints:")
            label.grid(row=number_of_rows + j, column=0, padx=10, pady=5)
            self.hint_labels.append(label)

            entry = tk.Entry(self.parent)
            entry.grid(row=number_of_rows + j, column=1, padx=10, pady=5)
            self.column_hints_entries.append(entry)

        self.create_board_button = tk.Button(
            self.parent, text="Create Board", command=self.create_board
        )
        self.create_board_button.grid(
            row=number_of_rows + number_of_columns, column=0, columnspan=2, pady=20
        )

    def create_board(self):
        row_hints = []
        for entry in self.row_hints_entries:
            hints = list(map(int, entry.get().split(",")))
            row_hints.append(hints)

        col_hints = []
        for entry in self.column_hints_entries:
            hints = list(map(int, entry.get().split(",")))
            col_hints.append(hints)

        try:
            board = NonoGramBoard(row_hints, col_hints)
            board.solve_board(verbose=False)
        except:
            messagebox.showerror(
                "Error",
                "The board is impossible to create. Please provide valid hints.",
            )
            return

        for label in self.hint_labels:
            label.destroy()
        for entry in self.row_hints_entries + self.column_hints_entries:
            entry.destroy()
        self.create_board_button.destroy()

        gui = NonoGramGUI(self.parent, board)
