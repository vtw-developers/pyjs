for i in range(n):
    myexactlog(4, 0)
    if flag is True:
        myexactlog(5, 0)
        temp[i] = arr[large]
        myexactlog(6, temp)
        large -= 1
        myexactlog(7, large)
    else:
        myexactlog(8, 0)
        temp[i] = arr[small]
        myexactlog(9, temp)
        small += 1
        myexactlog(10, small)
    flag = bool(1 - flag)
    myexactlog(11, flag)
    break