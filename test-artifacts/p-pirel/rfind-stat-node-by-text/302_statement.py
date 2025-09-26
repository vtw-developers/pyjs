if i == j and rem == j:
    myexactlog(10, 1)
    ans = ans + h[i] * (h[i] - 1) * (h[i] - 2) / 6
    myexactlog(11, ans)
elif i == j:
    myexactlog(12, 0)
    pass
elif rem == j:
    myexactlog(13, 1)
    pass
else:
    myexactlog(14, 0)
    pass