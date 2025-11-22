def test():
    params = [71, 71, 36, 3, 97, 69, 15, 48, 77, 6]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    count = 0
    count = (n + 1) * (n + 2) // 2
    return count
"-----------------"
test()