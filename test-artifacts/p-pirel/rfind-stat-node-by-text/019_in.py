def f_gold(m, n):
    T = [[0 for i in range(n + 1)] for i in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                T[i][j] = 0
            elif i < j:
                pass
            elif j == 1:
                pass
            else:
                pass