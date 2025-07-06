def f_gold(n):
    table = [0 for i in range(n + 1)]
    table[0] = 1
    for i in range(3, n + 1):
        table[i] += table[i - 3]
    for i in range(5, n + 1):
        table[i] += table[i - 5]
    for i in range(10, n + 1):
        table[i] += table[i - 10]
    return table[n]