def f_gold(n, p):
    ans = 0
    temp = p
    while temp <= n:
        ans += n / temp
        temp = temp * p
    return ans