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