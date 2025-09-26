def f_gold(N, insrt, remov, cpy):
    if N == 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    if N == 1:
        myexactlog(3, 1)
        myexactlog(4, insrt)
        return insrt
    dp = [0] * (N + 1)
    myexactlog(5, dp)
    for i in range(1, N + 1):
        myexactlog(6, 0)
        if i % 2 == 0:
            myexactlog(7, 2)
            dp[i] = min(dp[i - 1] + insrt, dp[i // 2] + cpy)
        else:
            pass