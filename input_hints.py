import tkinter as tk
from nonogram_solver import NonoGramBoard
from nonogram_gui import NonoGramGUI


class InputHints(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # Requesting board dimensions
        self.row_label = tk.Label(self, text="Number of Rows:")
        self.row_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.row_entry = tk.Entry(self)
        self.row_entry.grid(row=0, column=1, padx=10, pady=10)

        self.col_label = tk.Label(self, text="Number of Columns:")
        self.col_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.col_entry = tk.Entry(self)
        self.col_entry.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.get_dimensions)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=20)

    def get_dimensions(self):
        # Get the entered dimensions
        try:
            self.number_of_rows = int(self.row_entry.get())
            self.number_of_columns = int(self.col_entry.get())
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Please enter valid numbers for rows and columns."
            )
            return

        # Destroy existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Call the method to generate the hint input fields
        self.generate_hint_inputs()

    def generate_hint_inputs(self):
        # Generate input fields for row hints
        for i in range(self.number_of_rows):
            label = tk.Label(self, text=f"Row {i+1} Hints:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            # We can store these widgets in lists if we need to reference them later

        # Generate input fields for column hints
        for j in range(self.number_of_columns):
            label = tk.Label(self, text=f"Column {j+1} Hints:")
            label.grid(
                row=self.number_of_rows + j, column=0, padx=10, pady=5, sticky=tk.W
            )
            entry = tk.Entry(self)
            entry.grid(row=self.number_of_rows + j, column=1, padx=10, pady=5)
            # Just like before, we can store these widgets in lists

        # "Finish" button
        finish_button = tk.Button(self, text="Create Board", command=self.finish_setup)
        finish_button.grid(
            row=self.number_of_rows + self.number_of_columns + 1,
            column=0,
            columnspan=2,
            pady=20,
        )

    def finish_setup(self):
        # Gather the entered hints
        row_hints = []
        col_hints = []

        # For row hints
        for i in range(self.number_of_rows):
            entry = self.grid_slaves(row=i, column=1)[
                0
            ]  # Get the corresponding Entry widget
            hints = (
                entry.get().split()
            )  # We assume hints are entered separated by spaces
            try:
                row_hints.append([int(hint) for hint in hints])
            except ValueError:
                tk.messagebox.showerror(
                    "Error", f"Invalid hint for Row {i+1}. Please enter valid numbers."
                )
                return

        # For column hints
        for j in range(self.number_of_columns):
            entry = self.grid_slaves(row=self.number_of_rows + j, column=1)[
                0
            ]  # Get the corresponding Entry widget
            hints = (
                entry.get().split()
            )  # We assume hints are entered separated by spaces
            try:
                col_hints.append([int(hint) for hint in hints])
            except ValueError:
                tk.messagebox.showerror(
                    "Error",
                    f"Invalid hint for Column {j+1}. Please enter valid numbers.",
                )
                return

        # Create a new instance of NonoGramBoard for validation
        validation_board = NonoGramBoard(row_hints, col_hints)

        # Validate if the board can be solved
        try:
            validation_board.solve_board(verbose=False)
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"The board can't be solved. Please check your hints."
            )
            return

        # If everything is good, destroy all InputHints widgets and launch the board window
        for widget in self.winfo_children():
            widget.destroy()
        self.board_gui = NonoGramGUI(self.parent, NonoGramBoard(row_hints, col_hints))
