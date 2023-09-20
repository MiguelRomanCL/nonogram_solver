from typing import List


class NonoGramBoard:
    def __init__(self, row_hints: List[List[int]], col_hints: List[List[int]]):
        self.number_of_rows = len(row_hints)
        self.number_of_columns = len(col_hints)
        self.board = [
            [0 for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]
        self.row_hints = row_hints
        self.col_hints = col_hints

    def es_valido(self, linea, numeros):
        grupos = []
        grupo_actual = 0
        for celda in linea:
            if celda == -1:  # Si la celda está coloreada
                grupo_actual += 1
            elif grupo_actual:  # Si hemos terminado un grupo
                grupos.append(grupo_actual)
                grupo_actual = 0
        if grupo_actual:
            grupos.append(grupo_actual)
        return grupos == numeros

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
        for color in [-1, 1]:  # -1 representa # y 1 representa .
            self.board[fila][columna] = color
            if self.backtrack(fila, columna + 1):
                return True
            self.board[fila][columna] = 0
        return False

    def resolver(self):
        return self.backtrack()

    def mostrar_tablero(self):
        for fila in self.board:
            print(" ".join(["#" if c == -1 else "." if c == 1 else "?" for c in fila]))
