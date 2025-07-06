def f_gold(n, x):
    cnt = 0
    for i in range(1, n + 1):
        if i <= x:
            if x // i <= n and x % i == 0:
                cnt += 1
    return cnt