def f_gold(n):
    k = n
    imin = 1
    ans = 0
    while imin <= n:
        imax = n / k
        ans += k * (imax - imin + 1)
        imin = imax + 1
        k = n / imin
    return ans