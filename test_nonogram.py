from nonogram_solver import NonoGramBoard


# Etapa L
print("Etapa L")
row_hints = [[2], [3], [3], [4], [1, 3], [3], [6], [6, 2], [2], [1]]
col_hints = [[1], [3], [2], [1, 2], [2, 2], [7], [8], [2, 4], [1], [1]]
nonograma = NonoGramBoard(row_hints, col_hints)

if nonograma.resolver():
    nonograma.mostrar_tablero()
else:
    print("No se encontró una solución.")
