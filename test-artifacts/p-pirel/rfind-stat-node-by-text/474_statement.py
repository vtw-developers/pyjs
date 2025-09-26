for i in range(n):
    myexactlog(2, 1)
    prefix_sum = arr[i]
    myexactlog(3, prefix_sum)
    for j in range(i):
        myexactlog(4, 0)
        prefix_sum += arr[j]
        myexactlog(5, prefix_sum)
        break
    suffix_sum = arr[i]
    myexactlog(6, suffix_sum)
    j = n - 1
    myexactlog(7, j)
    while j > i:
        myexactlog(8, 0)
        suffix_sum += arr[j]
        myexactlog(9, suffix_sum)
        j -= 1
        myexactlog(10, j)
        break
    if prefix_sum == suffix_sum:
        myexactlog(11, 0)
        res = max(res, prefix_sum)
        myexactlog(12, res)
    break