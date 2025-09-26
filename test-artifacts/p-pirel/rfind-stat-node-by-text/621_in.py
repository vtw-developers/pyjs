def f_gold(arr, n):
    max_idx = n - 1
    myexactlog(1, max_idx)
    min_idx = 0
    myexactlog(2, min_idx)
    max_elem = arr[n - 1] + 1
    myexactlog(3, max_elem)
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
            min_idx += 1
            myexactlog(10, min_idx)
        break
    for i in range(0, n):
        myexactlog(11, 1)
        arr[i] = arr[i] / max_elem
        myexactlog(12, arr)
        break