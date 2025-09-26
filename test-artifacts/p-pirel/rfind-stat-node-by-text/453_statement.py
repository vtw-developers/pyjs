for i in range(n):
    myexactlog(4, 0)
    if arr[i] == 0:
        myexactlog(5, 0)
        sum_0 += -1
        myexactlog(6, sum_0)
    else:
        myexactlog(7, 0)
        sum_0 += 1
        myexactlog(8, sum_0)
    if sum_0 == 1:
        myexactlog(9, 1)
        maxLen = i + 1
        myexactlog(10, maxLen)
    elif sum_0 not in um:
        myexactlog(11, 0)
        um[sum_0] = i
        myexactlog(12, um)
    if (sum_0 - 1) in um:
        myexactlog(13, 2)
        pass
    break