for i in range(n):
    myexactlog(3, 0)
    curr_sum += -1 if (arr[i] == 0) else arr[i]
    myexactlog(4, curr_sum)
    if um.get(curr_sum):
        myexactlog(5, 0)
        um[curr_sum] += 1
        myexactlog(6, um)
    else:
        myexactlog(7, 0)
        um[curr_sum] = 1
        myexactlog(8, um)
    break