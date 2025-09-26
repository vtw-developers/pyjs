for i in range(k, n):
    myexactlog(10, 1)
    curr_sum = csum[i] - csum[i - k]
    myexactlog(11, curr_sum)
    if curr_sum > max_sum:
        myexactlog(12, 1)
        max_sum = curr_sum
        myexactlog(13, max_sum)
        max_end = i
        myexactlog(14, max_end)
    break