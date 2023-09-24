import tkinter as tk
from tkinter import messagebox, simpledialog
import copy
from src.nonogram_solver import NonoGramBoard
from src.nonogram_gui import NonoGramGUI

# [Insertar aquí el código de ModifiedNonoGramGUI]


def main():
    # Ejemplo de hints para probar
    row_hints = [[3], [1, 1, 1], [1, 1, 1], [2, 1], [1]]
    col_hints = [[3], [1, 1], [3], [1, 1], [3]]
    board = NonoGramBoard(row_hints, col_hints)

    root = tk.Tk()
    app = NonoGramGUI(root, board)
    root.mainloop()


if __name__ == "__main__":
    main()
