def test():
    params = [39, 20, 10, 39, 70, 21, 21, 80, 89, 99]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    S = 0
    for i in range(1, n + 1):
        S += i * i - (i - 1) * (i - 1)
    return S
"-----------------"
test()