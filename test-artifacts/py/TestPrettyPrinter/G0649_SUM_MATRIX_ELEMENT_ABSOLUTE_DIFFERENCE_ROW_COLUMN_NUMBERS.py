def f_gold(n):
    arr = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            arr[i][j] = abs(i - j)
    sum = 0
    for i in range(n):
        for j in range(n):
            sum += arr[i][j]
    return sum