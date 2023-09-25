import tkinter as tk
from tkinter import messagebox, simpledialog
import copy
from nonogram_solver import NonoGramBoard


class NonoGramGUI(tk.Frame):
    def __init__(self, parent, board):
        super().__init__(parent)
        self.parent = parent
        self.board = board
        self.original_board = copy.deepcopy(board)
        self.pack(fill=tk.BOTH, expand=True)

        # Intentamos resolver una copia del tablero y almacenar la solución
        try:
            self.solved_board_instance = copy.deepcopy(self.board)
            self.solved_board_instance.solve_board(verbose=False)
            self.solved_board = self.solved_board_instance.board
        except Exception as e:
            messagebox.showerror("Error", f"Error while solving the board: {str(e)}")
            self.solved_board = None

        self.number_of_rows = board.number_of_rows
        self.number_of_columns = board.number_of_columns
        self.buttons = [
            [None for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]

        self.create_widgets()
        self.create_solution_buttons()
        self.create_go_back_button()

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

    def mark_square(self, x, y, value):
        if self.board.board[x][y] == value:
            self.board.board[x][y] = None
        else:
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
            message = "The board is impossible to solve."
            messagebox.showinfo("Result", message)
            return

        is_correct = all(
            self.board.board[i][j] == self.solved_board[i][j]
            for i in range(self.number_of_rows)
            for j in range(self.number_of_columns)
        )

        if is_correct:
            message = "Correct solution!"
        else:
            message = "The solution is incorrect. Try again."
        messagebox.showinfo("Result", message)

    def check_solution(self):
        if self.solved_board is None:
            message = "The board is impossible to solve."
            messagebox.showinfo("Result", message)
            return

        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                self.board.board[i][j] = self.solved_board[i][j]
                self.update_button_color(i, j)

    def reset_board(self):
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                self.board.board[i][j] = None
                self.update_button_color(i, j)

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.show_welcome_screen()

    def create_go_back_button(self):
        go_back_button = tk.Button(self, text="Go Back", command=self.go_back)
        go_back_button.grid(
            row=self.number_of_rows + 3,
            column=0,
            pady=10,
            columnspan=self.number_of_columns + 1,
        )
