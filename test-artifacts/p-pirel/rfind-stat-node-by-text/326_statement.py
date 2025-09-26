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