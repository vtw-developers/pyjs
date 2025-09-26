for i in range(0, n):
    myexactlog(4, 0)
    if i % 2 == 0:
        myexactlog(5, 0)
        arr[i] += (arr[max_idx] % max_elem) * max_elem
        myexactlog(6, arr)
        max_idx -= 1
        myexactlog(7, max_idx)
    else:
        myexactlog(8, 0)
        arr[i] += (arr[min_idx] % max_elem) * max_elem
        myexactlog(9, arr)
    break