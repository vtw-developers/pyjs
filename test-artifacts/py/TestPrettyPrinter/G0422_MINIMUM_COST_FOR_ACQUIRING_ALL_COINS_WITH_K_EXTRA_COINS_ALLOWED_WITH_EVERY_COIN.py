import math
def f_gold(coin, n, k):
    coin.sort()
    coins_needed = math.ceil(1.0 * n // (k + 1))
    ans = 0
    for i in range(coins_needed - 1 + 1):
        ans += coin[i]
    return ans