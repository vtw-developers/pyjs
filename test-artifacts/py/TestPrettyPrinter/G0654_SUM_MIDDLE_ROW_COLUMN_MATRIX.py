def f_gold(mat, n):
    row_sum = 0
    col_sum = 0
    for i in range(n):
        row_sum += mat[n // 2][i]
    print("Sum of middle row = ", row_sum)
    for i in range(n):
        col_sum += mat[i][n // 2]
    print("Sum of middle column = ", col_sum)