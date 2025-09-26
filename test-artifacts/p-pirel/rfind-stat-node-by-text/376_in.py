def f_gold(arr, n):
    hash_map = {}
    myexactlog(1, hash_map)
    curr_sum = 0
    myexactlog(2, curr_sum)
    max_len = 0
    myexactlog(3, max_len)
    ending_index = -1
    myexactlog(4, ending_index)
    for i in range(0, n):
        myexactlog(5, 0)
        if arr[i] == 0:
            myexactlog(6, 0)
            arr[i] = -1
            myexactlog(7, arr)
        else:
            myexactlog(8, 0)
            arr[i] = 1
            myexactlog(9, arr)
        break
    for i in range(0, n):
        myexactlog(10, 1)
        curr_sum = curr_sum + arr[i]
        myexactlog(11, curr_sum)
        if curr_sum == 0:
            myexactlog(12, 1)
            max_len = i + 1
            myexactlog(13, max_len)
            ending_index = i
            myexactlog(14, ending_index)
        if curr_sum in hash_map:
            myexactlog(15, 2)
            pass
        else:
            myexactlog(16, 1)
            pass
        break