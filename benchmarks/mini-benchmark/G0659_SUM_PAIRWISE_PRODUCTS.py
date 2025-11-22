def test():
    params = [21, 32, 16, 38, 9, 3, 5, 46, 45, 87]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sm = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            sm = sm + i * j
    return sm
"-----------------"
test()