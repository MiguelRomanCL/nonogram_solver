class AlgorithmStuckException(Exception):
    pass


class IncongruentBoard(Exception):
    pass


class NonoGramBoard:
    def __init__(self, row_hints, col_hints):
        self.row_hints = row_hints
        self.col_hints = col_hints
        self.number_of_rows = len(row_hints)
        self.number_of_columns = len(col_hints)
        self.board = [
            [None for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)
        ]

    def board_is_complete(self):
        """Check if all cells of the board are non-null."""
        return all(cell is not None for row in self.board for cell in row)

    def board_is_congruent(self):
        # Verify every row against hints
        all_rows_valid = all(
            self.is_valid_line(self.board[i], self.row_hints[i])
            for i in range(self.number_of_rows)
        )

        # Verify every column against hints
        all_cols_valid = all(
            self.is_valid_line(
                [self.board[j][i] for j in range(self.number_of_rows)],
                self.col_hints[i],
            )
            for i in range(self.number_of_columns)
        )

        return all_rows_valid and all_cols_valid

    @staticmethod
    def find_common_positions(strings):
        length = len(strings[0])
        result = []
        for position in range(length):
            char = strings[0][position]
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

            if number_of_hints > 1:
                line += "0"
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

    # Define the modified find_possible_fills_partial_info function
    def find_possible_fills_partial_info(uncompleted_line, list_of_hints):
        list_of_possible_lines = NonoGramBoard.find_possible_fills(
            len(uncompleted_line), list_of_hints
        )

        def matches_uncompleted_line(line):
            return all(
                cell == int(line[i]) or cell is None
                for i, cell in enumerate(uncompleted_line)
            )

        filtered_lines = [
            line for line in list_of_possible_lines if matches_uncompleted_line(line)
        ]

        # Check if filtered_lines is empty and raise IncongruentBoard if it is
        if len(filtered_lines) == 0:
            raise IncongruentBoard(
                "The board is incongruent for the given hints and partial information."
            )

        return filtered_lines

    def fill_rows(self):
        for indice_filas in range(self.number_of_rows):
            row = self.board[indice_filas]
            hint_actual = self.row_hints[indice_filas]

            llenado_linea = [
                int(char) if char != "b" else None
                for char in NonoGramBoard.find_common_positions(
                    NonoGramBoard.find_possible_fills_partial_info(row, hint_actual)
                )
            ]

            for index, value in enumerate(llenado_linea):
                if value is not None:
                    self.board[indice_filas][index] = value

    def fill_columns(self):
        for indice_columnas in range(self.number_of_columns):
            column = [
                self.board[j][indice_columnas] for j in range(self.number_of_rows)
            ]
            hint_actual = self.col_hints[indice_columnas]

            llenado_linea = [
                int(char) if char != "b" else None
                for char in NonoGramBoard.find_common_positions(
                    NonoGramBoard.find_possible_fills_partial_info(column, hint_actual)
                )
            ]

            for index, value in enumerate(llenado_linea):
                if value is not None:
                    self.board[index][indice_columnas] = value

    def show_board(self):
        for fila in self.board:
            print(" ".join(["#" if c == 1 else "." if c == 0 else "?" for c in fila]))

    @staticmethod
    def is_valid_line(line, hints):
        groups = []
        group_count = 0
        for cell in line:
            if cell == 1:
                group_count += 1
            elif group_count:
                groups.append(group_count)
                group_count = 0
        if group_count:
            groups.append(group_count)
        return groups == hints

    def solve_board(self, verbose=True):
        iterations = 0
        while True:
            # Check if the board is complete and correct
            if self.board_is_complete():
                if self.board_is_congruent():
                    if verbose:
                        print(f"Solved the puzzle in {iterations} iterations.")
                        self.show_board()
                    return
                else:
                    raise IncongruentBoard(
                        "The board with the given hints cannot exist."
                    )
            iterations += 1
            # Create a deep copy of the current board
            board_copy = [row.copy() for row in self.board]

            # Try to fill rows and columns
            self.fill_rows()
            self.fill_columns()

            # Check if the board has changed
            if board_copy == self.board:
                # No changes made, raise UnresolvedBoardException
                raise AlgorithmStuckException(
                    "The algorithm is stuck and unable to progress further."
                )
