def test():
    params = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sum_0 = 0
    for row in range(n):
        sum_0 = sum_0 + (1 << row)
    return sum_0
"-----------------"
test()