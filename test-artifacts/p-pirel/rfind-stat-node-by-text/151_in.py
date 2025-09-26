def f_gold(arr, n):
    um = dict()
    myexactlog(1, um)
    curr_sum = 0
    myexactlog(2, curr_sum)
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
    count = 0
    myexactlog(9, count)
    for itr in um:
        myexactlog(10, 1)
        if um[itr] > 1:
            myexactlog(11, 1)
            count += (um[itr] * int(um[itr] - 1)) / 2
            myexactlog(12, count)
        break
    if um.get(0):
        myexactlog(13, 2)
        count += um[0]
        myexactlog(14, count)
    retval_1 = int(count)
    myexactlog(15, retval_1)
    myexactlog(16, retval_1)
    return retval_1