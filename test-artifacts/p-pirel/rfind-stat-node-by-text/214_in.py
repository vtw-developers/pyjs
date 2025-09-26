def f_gold(arr, n):
    res = -sys.maxsize - 1
    myexactlog(1, res)
    for i in range(n):
        myexactlog(2, 1)
        prefix_sum = arr[i]
        myexactlog(3, prefix_sum)
        for j in range(i):
            myexactlog(4, 0)
            prefix_sum += arr[j]
            myexactlog(5, prefix_sum)
            break
        break