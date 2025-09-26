for i in range(n):
    myexactlog(1, 0)
    curr_sum = arr[i]
    myexactlog(2, curr_sum)
    j = i + 1
    myexactlog(3, j)
    while j <= n and curr_sum <= sum_0:
        myexactlog(4, 0)
        if curr_sum == sum_0:
            myexactlog(5, 0)
            pass
        break
    break