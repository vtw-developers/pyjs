def test():
    params = [1, 5, 14, 140, 204, 3, 506, 42, 4, 87]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(s):
    _sum = 0
    n = 1
    while _sum < s:
        _sum += n * n
        n += 1
    n -= 1
    if _sum == s:
        return n
    return -1
"-----------------"
test()