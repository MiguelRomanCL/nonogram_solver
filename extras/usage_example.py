from src.nonogram_solver import NonoGramBoard

# Define hints for rows and columns
row_hints = [[5], [2], [2], [2], [2]]
col_hints = [[1], [1, 1], [1, 3], [3, 1], [2]]

# Create an instance of the solver
nonogram = NonoGramBoard(row_hints, col_hints)

# Solve the nonogram
nonogram.solve_board(verbose=True)
