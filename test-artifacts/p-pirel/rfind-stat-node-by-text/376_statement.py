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