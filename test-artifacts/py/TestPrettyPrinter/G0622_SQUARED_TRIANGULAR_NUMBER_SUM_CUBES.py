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