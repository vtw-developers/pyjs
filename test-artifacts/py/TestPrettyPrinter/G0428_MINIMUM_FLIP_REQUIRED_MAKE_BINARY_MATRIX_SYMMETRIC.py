def f_gold(mat, n):
    transpose = [[0] * n] * n
    for i in range(n):
        for j in range(n):
            transpose[i][j] = mat[j][i]
    flip = 0
    for i in range(n):
        for j in range(n):
            if transpose[i][j] != mat[i][j]:
                flip += 1
    return int(flip / 2)