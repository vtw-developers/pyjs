import math
def f_gold(n):
    ans = 0
    for length in range(1, int(math.sqrt(n)) + 1):
        height = length
        while height * length <= n:
            ans += 1
            height += 1
    return ans