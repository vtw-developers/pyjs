def f_gold(f, d, s):
    mem = [[0 for i in range(s + 1)] for j in range(d + 1)]
    mem[0][0] = 1
    for i in range(1, d + 1):
        for j in range(1, s + 1):
            mem[i][j] = mem[i][j - 1] + mem[i - 1][j - 1]
            if j - f - 1 >= 0:
                mem[i][j] -= mem[i - 1][j - f - 1]
    return mem[d][s]