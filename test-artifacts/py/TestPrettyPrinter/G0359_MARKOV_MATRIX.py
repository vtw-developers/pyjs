def f_gold(m):
    for i in range(0, len(m)):
        sm = 0
        for j in range(0, len(m[i])):
            sm = sm + m[i][j]
        if sm != 1:
            return False
    return True