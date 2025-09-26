def f_gold(n):
    res = 1
    myexactlog(1, res)
    for i in range(0, n):
        myexactlog(2, 0)
        res *= 2 * n - i
        myexactlog(3, res)
        res /= i + 1
        myexactlog(4, res)
        break
    retval_1 = res / (n + 1)