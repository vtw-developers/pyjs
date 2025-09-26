def f_gold(n, r, b, g):
    fact = [0 for i in range(n + 1)]
    myexactlog(1, fact)
    fact[0] = 1
    myexactlog(2, fact)
    for i in range(1, n + 1, 1):
        myexactlog(3, 0)
        fact[i] = fact[i - 1] * i
        myexactlog(4, fact)
        break
    left = n - (r + g + b)
    myexactlog(5, left)
    sum_0 = 0
    myexactlog(6, sum_0)
    for i in range(0, left + 1, 1):
        myexactlog(7, 2)
        for j in range(0, left - i + 1, 1):
            myexactlog(8, 1)
            k = left - (i + j)
            myexactlog(9, k)
            sum_0 = sum_0 + fact[n] / (fact[i + r] * fact[j + b] * fact[k + g])
            myexactlog(10, sum_0)
            break
        break