### Mundo 1


# Etapa A
row_hints = [[5], [2], [2], [2], [2]]
col_hints = [[1], [1, 1], [1, 3], [3, 1], [2]]


# Etapa B
row_hints = [[1, 2], [1, 2], [1, 2], [3], [3]]
col_hints = [[3], [1], [2], [5], [4]]


# Etapa C
row_hints = [[1], [5], [2], [3], [2, 1]]
col_hints = [[1, 1], [1, 2], [3], [5], [1]]


# Etapa D
row_hints = [[3], [1, 1, 1], [1, 1, 1], [2, 1], [1]]
col_hints = [[3], [1, 1], [3], [1, 1], [3]]

# Etapa E
row_hints = [[2, 2], [2, 1, 1], [2, 1, 1], [10], [9], [2], [2], [3], [8], [7]]
col_hints = [
    [8],
    [9],
    [2, 3],
    [2, 2],
    [2, 2],
    [2, 2],
    [4, 2],
    [1, 2, 2],
    [1, 2, 2],
    [3],
]

# Etapa F
row_hints = [[7], [8], [4, 2], [4, 3], [3, 4], [4], [4], [4], [5], [3]]
col_hints = [[2], [3, 1], [4, 2], [4, 3], [3, 4], [2, 4], [2, 4], [2, 4], [6], [5]]

# Etapa G
row_hints = [[0], [8], [8], [2, 2], [2, 2], [2, 2], [2, 2], [8], [8], [0]]
col_hints = [[0], [8], [8], [2, 2], [2, 2], [2, 2], [2, 2], [8], [8], [0]]

# Etapa H
row_hints = []
col_hints = []


# Etapa I
row_hints = []
col_hints = []

# Etapa J
row_hints = []
col_hints = []

# Etapa K
row_hints = []
col_hints = []


# Etapa L
row_hints = [[2], [3], [3], [4], [1, 3], [3], [6], [6, 2], [2], [1]]
col_hints = [[1], [3], [2], [1, 2], [2, 2], [7], [8], [2, 4], [1], [1]]


row_hints = [[5], [2], [2], [2], [2]]
col_hints = [[1], [1, 1], [1, 3], [3, 1], [2]]


from src.nonogram_solver import NonoGramBoard

nonograma = NonoGramBoard(row_hints, col_hints)
