def test():
    params = [76, 91, 62, 65, 83, 57, 76, 6, 2, 86]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    prevPrev = 1
    prev = 2
    curr = 3
    while n > 0:
        prevPrev = prev
        prev = curr
        curr = prevPrev + prev
        n = n - (curr - prev - 1)
    n = n + (curr - prev - 1)
    return prev + n
"-----------------"
test()