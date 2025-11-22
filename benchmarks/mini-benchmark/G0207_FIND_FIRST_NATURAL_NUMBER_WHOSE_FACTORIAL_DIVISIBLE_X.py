def test():
    params = [6, 4, 5, 9, 7, 2, 1, 3, 8, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    k = 1
    fact = 1
    for i in range(1, x):
        k = i
        fact = fact * i
        if fact % x == 0:
            break
    return k
"-----------------"
test()