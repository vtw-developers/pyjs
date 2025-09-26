def f_gold(mat, r, c):
    a = 0
    b = 2
    low_row = 0 if (0 > a) else a
    low_column = 0 if (0 > b) else b - 1
    high_row = r - 1 if ((a + 1) >= r) else a + 1
    high_column = c - 1 if ((b + 1) >= c) else b + 1
    while low_row > 0 - r and low_column > 0 - c:
        i = low_column + 1
        while i <= high_column and i < c and low_row >= 0:
            print(mat[low_row][i], end=" ")
            i += 1
        low_row -= 1
        i = low_row + 2
        while i <= high_row and i < r and high_column < c:
            print(mat[i][high_column], end=" ")
            i += 1
        high_column += 1
        i = high_column - 2
        while i >= low_column and i >= 0 and high_row < r:
            print(mat[high_row][i], end=" ")
            i -= 1
        high_row += 1
        i = high_row - 2
        while i > low_row and i >= 0 and low_column >= 0:
            print(mat[i][low_column], end=" ")
            i -= 1
        low_column -= 1