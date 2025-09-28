def f_gold(n, index, Sum, M, arr, dp):
    if index == n:
        myexactlog(1, 1)
        if (Sum % M) == 0:
            myexactlog(2, 0)
            myexactlog(3, True)
            return True
        myexactlog(4, False)
        return False
    if Sum in dp[index]:
        myexactlog(5, 2)
        pass