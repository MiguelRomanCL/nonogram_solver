from typing import List


class NonoGramBoard:
    def __init__(self, row_hints: List[List[int]], col_hints: List[List[int]]):
        self.number_of_rows = len(row_hints)
        self.number_of_columns = len(col_hints)
        self.board = [
            [None for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]
        self.completed_board = [
            [None for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]
        self.row_hints = row_hints
        self.col_hints = col_hints

    def agrupar_linea(self, linea):
        grupos = []
        grupo_actual = 0
        for celda in linea:
            if celda == 1:  # Si la celda está coloreada
                grupo_actual += 1
            elif grupo_actual:  # Si hemos terminado un grupo
                grupos.append(grupo_actual)
                grupo_actual = 0
        if grupo_actual:
            grupos.append(grupo_actual)
        return grupos

    def es_valido(self, linea, numeros):
        return self.agrupar_linea(linea) == numeros

    def es_posible(self, linea, numeros):
        return sum(self.agrupar_linea(linea)) <= sum(numeros)

    def es_tablero_valido(self):
        # Verificar cada fila
        for i in range(self.number_of_rows):
            if not self.es_valido(self.board[i], self.row_hints[i]):
                return False
        # Verificar cada columna
        for i in range(self.number_of_columns):
            if not self.es_valido(
                [self.board[j][i] for j in range(self.number_of_rows)],
                self.col_hints[i],
            ):
                return False
        return True

    def mostrar_tablero(self):
        for fila in self.board:
            print(" ".join(["#" if c == 1 else "." if c == 0 else "?" for c in fila]))

    def backtrack(self, fila=0, columna=0):
        if fila == self.number_of_rows:
            return all(
                self.es_valido(self.board[i], self.row_hints[i])
                and self.es_valido(
                    [self.board[j][i] for j in range(self.number_of_rows)],
                    self.col_hints[i],
                )
                for i in range(self.number_of_rows)
            )
        if columna == self.number_of_columns:
            return self.backtrack(fila + 1, 0)

        # Skip determined cells
        if abs(self.board[fila][columna]) == 2:
            return self.backtrack(fila, columna + 1)

        for color in [1, 0]:  # -1 represents # and 1 represents.
            self.board[fila][columna] = color
            # Check if the current row and column are possible
            if self.es_posible(
                self.board[fila], self.row_hints[fila]
            ) and self.es_posible(
                [self.board[j][columna] for j in range(self.number_of_rows)],
                self.col_hints[columna],
            ):
                if self.backtrack(fila, columna + 1):
                    return True
            self.board[fila][columna] = None
        return False

    def resolver(self):
        return self.backtrack()
