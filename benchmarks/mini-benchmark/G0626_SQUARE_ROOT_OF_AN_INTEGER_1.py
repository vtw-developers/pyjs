def test():
    params = [40, 10, 46, 54, 1, 67, 64, 10, 75, 11]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    if x == 0 or x == 1:
        return x
    start = 1
    end = x
    ans = 0
    while start <= end:
        mid = (start + end) // 2
        if mid * mid == x:
            return mid
        if mid * mid < x:
            start = mid + 1
            ans = mid
        else:
            end = mid - 1
    return ans
"-----------------"
test()