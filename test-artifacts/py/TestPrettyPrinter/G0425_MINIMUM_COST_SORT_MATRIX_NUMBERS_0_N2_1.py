def f_gold(mat, n):
    tot_energy = 0
    for i in range(n):
        for j in range(n):
            q = mat[i][j] // n
            i_des = q
            j_des = mat[i][j] - (n * q)
            tot_energy += abs(i_des - i) + abs(j_des - j)
    return tot_energy