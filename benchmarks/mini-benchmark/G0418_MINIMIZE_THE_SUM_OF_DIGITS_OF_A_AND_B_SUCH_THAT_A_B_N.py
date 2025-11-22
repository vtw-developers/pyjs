def test():
    params = [2, 39, 31, 45, 35, 94, 67, 50, 4, 63, 1]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sum_0 = 0
    while n > 0:
        sum_0 += n % 10
        n //= 10
    if sum_0 == 1:
        return 10
    return sum_0
"-----------------"
test()