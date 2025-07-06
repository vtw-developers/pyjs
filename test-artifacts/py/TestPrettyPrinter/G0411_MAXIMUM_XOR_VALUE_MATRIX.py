def f_gold(mat, N):
    max_xor = 0
    for i in range(N):
        r_xor = 0
        c_xor = 0
        for j in range(N):
            r_xor = r_xor ^ mat[i][j]
            c_xor = c_xor ^ mat[j][i]
        if max_xor < max(r_xor, c_xor):
            max_xor = max(r_xor, c_xor)
    return max_xor