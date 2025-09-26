def f_gold(arr, n, k):
    count_map = {}
    myexactlog(1, count_map)
    for i in range(0, n):
        myexactlog(2, 0)
        if arr[i] in count_map.keys():
            myexactlog(3, 0)
            count_map[arr[i]] += 1
            myexactlog(4, count_map)
        else:
            myexactlog(5, 0)
            count_map[arr[i]] = 1
            myexactlog(6, count_map)
        i += 1
        myexactlog(7, i)
        break
    for i in range(0, n):
        myexactlog(8, 1)
        if count_map[arr[i]] == k:
            myexactlog(9, 1)
            pass
        break