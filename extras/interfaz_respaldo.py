import tkinter as tk
from tkinter import simpledialog, messagebox
from src.nonogram_solver import NonoGramBoard
import copy


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NonoGram Start")
        self.geometry("300x100")

        self.label = tk.Label(self, text="Welcome to NonoGram!")
        self.label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(pady=10)

    def start(self):
        self.destroy()
        input_hints = InputHints(self)
        input_hints.mainloop()


class InputHints(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Input Hints")

        self.row_var = tk.StringVar()
        self.column_var = tk.StringVar()

        self.label1 = tk.Label(self, text="Number of Rows:")
        self.label1.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.row_entry = tk.Entry(self, textvariable=self.row_var)
        self.row_entry.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.label2 = tk.Label(self, text="Number of Columns:")
        self.label2.grid(row=0, column=1, padx=20, pady=(20, 0))

        self.column_entry = tk.Entry(self, textvariable=self.column_var)
        self.column_entry.grid(row=1, column=1, padx=20, pady=(0, 20))

        self.submit_button = tk.Button(self, text="Next", command=self.create_hint_grid)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=20)

    def create_hint_grid(self):
        try:
            number_of_rows = int(self.row_var.get())
            number_of_columns = int(self.column_var.get())

            for widget in self.winfo_children():
                widget.destroy()

            self.entries = []

            for i in range(number_of_rows):
                entry = tk.Entry(self)
                entry.grid(row=i, column=0, padx=10, pady=10)
                self.entries.append(entry)

            for j in range(number_of_columns):
                entry = tk.Entry(self)
                entry.grid(row=number_of_rows, column=j + 1, padx=10, pady=10)
                self.entries.append(entry)

            self.submit_hints_button = tk.Button(
                self,
                text="Submit Hints",
                command=lambda: self.submit_hints(number_of_rows, number_of_columns),
            )
            self.submit_hints_button.grid(
                row=number_of_rows + 1,
                column=0,
                columnspan=number_of_columns + 1,
                pady=20,
            )

        except ValueError:
            messagebox.showerror(
                "Error", "Please enter valid numbers for rows and columns."
            )

    def submit_hints(self, number_of_rows, number_of_columns):
        try:
            row_hints = [
                list(map(int, entry.get().split(",")))
                for entry in self.entries[:number_of_rows]
            ]
            col_hints = [
                list(map(int, entry.get().split(",")))
                for entry in self.entries[number_of_rows:]
            ]

            nonogram = NonoGramBoard(row_hints, col_hints)
            try:
                nonogram.solve_board(verbose=False)
                self.destroy()
                app = NonoGramGUI(nonogram)
                app.mainloop()
            except Exception as e:
                messagebox.showwarning(
                    "Warning",
                    f"The board is impossible to create due to {str(e)}.\nPlease provide valid hints.",
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid hints. Use ',' to separate hints for a row or column.",
            )


class NonoGramGUI(tk.Frame):
    def __init__(self, master, board):
        super().__init__(master)
        self.master = master
        self.board = board
        self.original_board = copy.deepcopy(board)
        self.pack(fill=tk.BOTH, expand=True)

        # Attempt to solve the board and store the solution
        try:
            self.solved_board = copy.deepcopy(self.board.board)
            self.board.solve_board(verbose=False)
        except Exception as e:
            print(f"Alert: The board is {str(e)}")
            self.solved_board = None

        self.number_of_rows = board.number_of_rows
        self.number_of_columns = board.number_of_columns
        self.buttons = [
            [None for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]

        self.create_widgets()
        self.create_solution_buttons()

    def create_widgets(self):
        for j, col_hint in enumerate(self.board.col_hints):
            hint_str = "-".join(map(str, col_hint))
            label = tk.Label(self, text=hint_str, padx=10, pady=10)
            label.grid(row=0, column=j + 1, sticky=tk.W + tk.E)

        for i in range(self.number_of_rows):
            hint_str = "-".join(map(str, self.board.row_hints[i]))
            label = tk.Label(self, text=hint_str, padx=10, pady=10)
            label.grid(row=i + 1, column=0, sticky=tk.W + tk.E)

            for j in range(self.number_of_columns):
                btn = tk.Button(
                    self,
                    width=4,
                    height=2,
                    bg="gray",
                    command=lambda x=i, y=j: self.mark_square(x, y, 1),
                )
                btn.bind(
                    "<Button-3>", lambda event, x=i, y=j: self.mark_square(x, y, 0)
                )
                btn.grid(row=i + 1, column=j + 1, sticky=tk.W + tk.E)
                self.buttons[i][j] = btn

        # Configure columns to use uniform space
        for col in range(self.number_of_columns + 1):
            self.grid_columnconfigure(col, weight=1)

    def create_solution_buttons(self):
        send_solution_btn = tk.Button(
            self, text="Send Solution", command=self.send_solution
        )
        send_solution_btn.grid(
            row=self.number_of_rows + 1,
            column=0,
            pady=10,
            columnspan=(self.number_of_columns + 1) // 2,
        )

        check_solution_btn = tk.Button(
            self, text="Check Solution", command=self.check_solution
        )
        check_solution_btn.grid(
            row=self.number_of_rows + 1,
            column=(self.number_of_columns + 1) // 2,
            pady=10,
            columnspan=self.number_of_columns // 2,
        )

        reset_board_btn = tk.Button(self, text="Reset Board", command=self.reset_board)
        reset_board_btn.grid(
            row=self.number_of_rows + 2,
            column=0,
            pady=10,
            columnspan=self.number_of_columns + 1,
        )

    def mark_square(self, x: int, y: int, value: int):
        self.board.board[x][y] = value
        self.update_button_color(x, y)

    def update_button_color(self, x, y):
        value = self.board.board[x][y]
        if value is None:
            color = "gray"
        elif value == 1:
            color = "red"
        else:  # value == 0
            color = "green"
        self.buttons[x][y].config(bg=color)

    def send_solution(self):
        if self.solved_board is None:
            message = "The board could not be solved."
            tk.messagebox.showinfo("Result", message)
            return

        is_correct = self.board.board == self.solved_board
        if is_correct:
            message = "Correct solution!"
        else:
            message = "The solution is incorrect. Try again."
        tk.messagebox.showinfo("Result", message)

    def check_solution(self):
        if self.solved_board is None:
            message = "The board could not be solved."
            tk.messagebox.showinfo("Result", message)
            return

        self.board.board = [row.copy() for row in self.solved_board]
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                self.update_button_color(i, j)

    def reset_board(self):
        self.board.board = [row.copy() for row in self.original_board.board]
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                self.update_button_color(i, j)


# When starting the app:
root = tk.Tk()
root.title("NonoGram")
app = MainApplication()
root.mainloop()
