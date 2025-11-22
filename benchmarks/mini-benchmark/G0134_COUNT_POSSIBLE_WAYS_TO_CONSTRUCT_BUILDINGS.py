def test():
    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(N):
    if N == 1:
        return 4
    countB = 1
    countS = 1
    for i in range(2, N + 1):
        prev_countB = countB
        prev_countS = countS
        countS = prev_countB + prev_countS
        countB = prev_countS
    result = countS + countB
    ret_val = result * result
    return ret_val
"-----------------"
test()