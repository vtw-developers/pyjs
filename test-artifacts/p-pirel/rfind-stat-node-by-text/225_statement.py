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