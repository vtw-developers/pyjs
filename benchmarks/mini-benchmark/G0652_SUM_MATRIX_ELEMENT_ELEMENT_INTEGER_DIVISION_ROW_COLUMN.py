def test():
    params = [60, 74, 8, 74, 34, 66, 96, 11, 45, 72]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(N):
    ans = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            ans += i // j
    return ans
"-----------------"
test()