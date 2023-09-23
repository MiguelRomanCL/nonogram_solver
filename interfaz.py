import tkinter as tk
from nonogram_solver import NonoGramBoard
from tkinter import messagebox
import copy


class NonoGramGUI(tk.Tk):
    def __init__(self, board: NonoGramBoard):
        super().__init__()
        self.board = board
        self.title("NonoGram")

        self.number_of_rows = board.number_of_rows
        self.number_of_columns = board.number_of_columns

        # Create a separate board instance for solving
        solve_board_instance = NonoGramBoard(board.row_hints, board.col_hints)
        try:
            solve_board_instance.solve_board(verbose=False)
            # Make a deep copy of the solved board
            self.solved_board = copy.deepcopy(solve_board_instance.board)
        except Exception as e:
            print(f"Alert: The board is {str(e)}")
            self.solved_board = None

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


if __name__ == "__main__":
    # Example usage
    row_hints = [[7], [8], [4, 2], [4, 3], [3, 4], [4], [4], [4], [5], [3]]
    col_hints = [[2], [3, 1], [4, 2], [4, 3], [3, 4], [2, 4], [2, 4], [2, 4], [6], [5]]

    # Example usage
    nonogram = NonoGramBoard(row_hints, col_hints)

    app = NonoGramGUI(nonogram)
    app.mainloop()
