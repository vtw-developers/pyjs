def f_gold(mat, N):
    for row in range(N):
        for col in range(N):
            if row == col and mat[row][col] != 1:
                return False
            elif row != col and mat[row][col] != 0:
                return False
    return True