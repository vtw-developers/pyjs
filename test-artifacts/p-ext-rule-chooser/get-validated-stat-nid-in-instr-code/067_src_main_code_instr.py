def f_gold(s1, s2):
    n = len(s1)
    myexactlog(1, n)
    m = len(s2)
    myexactlog(2, m)
    dp = [[False for i in range(m + 1)] for i in range(n + 1)]
    myexactlog(3, dp)