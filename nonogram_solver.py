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
                for i in range(self.number_of_rows)
            ) and all(
                self.es_valido(
                    [self.board[j][i] for j in range(self.number_of_rows)],
                    self.col_hints[i],
                )
                for i in range(self.number_of_columns)
            )
        for value in (0, 1):
            self.board[fila][columna] = value
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

    @staticmethod
    def find_common_positions(strings):
        """Find positions where all strings coincide and their values."""
        # Assuming all strings are of the same length
        length = len(strings[0])

        result = []

        for position in range(length):
            # Get the character at the current position for the first string
            char = strings[0][position]

            # Check if all other strings have the same character at the same position
            if all(s[position] == char for s in strings[1:]):
                result.append(char)
            else:
                result.append("b")

        return "".join(result)

    @staticmethod
    def find_possible_fills(length_of_line, list_of_hints):
        empty_spaces = length_of_line - sum(list_of_hints)
        number_of_hints = len(list_of_hints)
        filler_spaces = empty_spaces - number_of_hints + 1

        list_of_possible_lines = []
        for initial_left_space in range(filler_spaces + 1):
            line = ""
            line += "0" * initial_left_space
            line += "1" * list_of_hints[0]

            number_of_hints -= 1

            if number_of_hints > 0:
                line += "0"

            if number_of_hints > 0:
                list_of_possible_sub_lines = NonoGramBoard.find_possible_fills(
                    length_of_line - len(line), list_of_hints[1:]
                )
                extended_lines = [
                    line + sub_line for sub_line in list_of_possible_sub_lines
                ]
                list_of_possible_lines += extended_lines

            else:
                line += "0" * (length_of_line - len(line))
                list_of_possible_lines.append(line)

        return list_of_possible_lines
