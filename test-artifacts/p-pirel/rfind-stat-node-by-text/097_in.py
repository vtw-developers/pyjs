def f_gold(arr, n):
    arr.sort()
    myexactlog(1, arr)
    count = 0
    myexactlog(2, count)
    max_count = 0
    myexactlog(3, max_count)
    min_count = n
    myexactlog(4, min_count)
    for i in range(0, (n - 1)):
        myexactlog(5, 0)
        if arr[i] == arr[i + 1]:
            myexactlog(6, 0)
            count += 1
            myexactlog(7, count)
            continue
        else:
            myexactlog(8, 0)
            max_count = max(max_count, count)
            myexactlog(9, max_count)
            min_count = min(min_count, count)
            myexactlog(10, min_count)
            count = 0