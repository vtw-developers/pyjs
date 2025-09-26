for j in range(i + 1, n):
    myexactlog(3, 1)
    for k in range(j + 1, n):
        myexactlog(4, 0)
        if sm < (arr[i] + arr[j] + arr[k]):
            myexactlog(5, 0)
            pass
        break
    break