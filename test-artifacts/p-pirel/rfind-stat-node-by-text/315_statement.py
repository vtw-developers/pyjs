for j in range(i, n):
    myexactlog(5, 0)
    if j == i:
        myexactlog(6, 0)
        a[j] = 1
        myexactlog(7, a)
    elif s[i] == s[j]:
        myexactlog(8, 0)
        temp = a[j]
        myexactlog(9, temp)
    else:
        myexactlog(10, 0)
        pass
    break