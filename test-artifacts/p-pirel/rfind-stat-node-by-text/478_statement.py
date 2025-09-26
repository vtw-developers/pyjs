for i in range(0, M):
    myexactlog(6, 2)
    for j in range(i, M):
        myexactlog(7, 1)
        rem = (M - (i + j) % M) % M
        myexactlog(8, rem)
        if rem < j:
            myexactlog(9, 0)
            continue
        if i == j and rem == j:
            myexactlog(10, 1)
            ans = ans + h[i] * (h[i] - 1) * (h[i] - 2) / 6
            myexactlog(11, ans)
        elif i == j:
            myexactlog(12, 0)
            ans = ans + (h[i] * (h[i] - 1) * h[rem] / 2)
            myexactlog(13, ans)
        elif rem == j:
            myexactlog(14, 1)
            pass
        else:
            myexactlog(15, 0)
            pass
        break
    break