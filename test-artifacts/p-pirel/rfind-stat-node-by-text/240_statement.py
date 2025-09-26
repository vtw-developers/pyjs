for i in range(n):
    myexactlog(2, 0)
    j = 0
    myexactlog(3, j)
    while j < n:
        myexactlog(4, 0)
        if i != j and arr[j] == arr[i]:
            myexactlog(5, 0)
            pass
        break
    break