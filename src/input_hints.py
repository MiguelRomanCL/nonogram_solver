import tkinter as tk
from nonogram_solver import NonoGramBoard
from nonogram_gui import NonoGramGUI


class InputHints(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # Solicitando las dimensiones del tablero
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
        # Obtener las dimensiones ingresadas
        try:
            self.number_of_rows = int(self.row_entry.get())
            self.number_of_columns = int(self.col_entry.get())
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Please enter valid numbers for rows and columns."
            )
            return

        # Destruir widgets existentes
        for widget in self.winfo_children():
            widget.destroy()

        # Llamamos al método para generar los campos de entrada de hints
        self.generate_hint_inputs()

    def generate_hint_inputs(self):
        # Generar campos de entrada para hints de fila
        for i in range(self.number_of_rows):
            label = tk.Label(self, text=f"Row {i+1} Hints:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            # Podemos almacenar estos widgets en listas si necesitamos referenciarlos más tarde

        # Generar campos de entrada para hints de columna
        for j in range(self.number_of_columns):
            label = tk.Label(self, text=f"Column {j+1} Hints:")
            label.grid(
                row=self.number_of_rows + j, column=0, padx=10, pady=5, sticky=tk.W
            )
            entry = tk.Entry(self)
            entry.grid(row=self.number_of_rows + j, column=1, padx=10, pady=5)
            # Al igual que antes, podemos almacenar estos widgets en listas

        # Botón "Finalizar"
        finish_button = tk.Button(self, text="Create Board", command=self.finish_setup)
        finish_button.grid(
            row=self.number_of_rows + self.number_of_columns + 1,
            column=0,
            columnspan=2,
            pady=20,
        )

    def finish_setup(self):
        # Recopilar los hints ingresados
        row_hints = []
        col_hints = []

        # Para los hints de fila
        for i in range(self.number_of_rows):
            entry = self.grid_slaves(row=i, column=1)[
                0
            ]  # Obtener el Entry widget correspondiente
            hints = (
                entry.get().split()
            )  # Asumimos que los hints se ingresan separados por espacios
            try:
                row_hints.append([int(hint) for hint in hints])
            except ValueError:
                tk.messagebox.showerror(
                    "Error", f"Invalid hint for Row {i+1}. Please enter valid numbers."
                )
                return

        # Para los hints de columna
        for j in range(self.number_of_columns):
            entry = self.grid_slaves(row=self.number_of_rows + j, column=1)[
                0
            ]  # Obtener el Entry widget correspondiente
            hints = (
                entry.get().split()
            )  # Asumimos que los hints se ingresan separados por espacios
            try:
                col_hints.append([int(hint) for hint in hints])
            except ValueError:
                tk.messagebox.showerror(
                    "Error",
                    f"Invalid hint for Column {j+1}. Please enter valid numbers.",
                )
                return

        # Crear una instancia de NonoGramBoard con los hints proporcionados
        board = NonoGramBoard(row_hints, col_hints)

        # Destruir todos los widgets de InputHints
        for widget in self.winfo_children():
            widget.destroy()

        # Lanzar la ventana del tablero
        self.board_gui = NonoGramGUI(self.parent, board)
