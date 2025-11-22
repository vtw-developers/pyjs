def test():
    params = [15, 36, 39, 43, 75, 49, 56, 14, 62, 97]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(s):
    _sum = 0
    n = 1
    while _sum < s:
        _sum += n * n * n
        n += 1
    n -= 1
    if _sum == s:
        return n
    return -1
"-----------------"
test()