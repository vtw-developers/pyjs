def f_gold(x, y, n):
    sum = 0
    for i in range(n):
        for j in range(i + 1, n):
            sum += abs(x[i] - x[j]) + abs(y[i] - y[j])
    return sum