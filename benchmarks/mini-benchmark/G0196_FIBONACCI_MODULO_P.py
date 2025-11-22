def test():
    params = [51, 40, 68, 7, 8, 32, 93, 75, 71, 15]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(p):
    first = 1
    second = 1
    number = 2
    next_0 = 1
    while next_0 != 0:
        next_0 = (first + second) % p
        first = second
        second = next_0
        number = number + 1
    return number
"-----------------"
test()