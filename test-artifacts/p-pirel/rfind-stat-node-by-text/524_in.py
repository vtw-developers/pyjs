def f_gold(arr, n):
    um = {i: 0 for i in range(10)}
    myexactlog(1, um)
    sum_0 = 0
    myexactlog(2, sum_0)
    maxLen = 0
    myexactlog(3, maxLen)
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
            myexactlog(13, 3)
            if maxLen < (i - um[sum_0 - 1]):
                myexactlog(14, 2)
                pass