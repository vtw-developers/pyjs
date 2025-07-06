def f_gold(mat, row, column):
    print("Diagonal one : ", end="")
    for i in range(0, row):
        for j in range(0, column):
            if i == j:
                print("{} ".format(mat[i][j] * mat[i][j]), end="")
    print(" \n\nDiagonal two : ", end="")
    for i in range(0, row):
        for j in range(0, column):
            if i + j == column - 1:
                print("{} ".format(mat[i][j] * mat[i][j]), end="")