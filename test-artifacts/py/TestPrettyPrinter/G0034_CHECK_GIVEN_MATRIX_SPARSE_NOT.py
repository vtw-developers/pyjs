def f_gold(array, m, n):
    counter = 0
    for i in range(0, m):
        for j in range(0, n):
            if array[i][j] == 0:
                counter = counter + 1
    return counter > ((m * n) // 2)