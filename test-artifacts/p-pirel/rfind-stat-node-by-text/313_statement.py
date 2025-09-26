for i in range(0, n):
    myexactlog(4, 0)
    while A[i] in mp:
        myexactlog(5, 0)
        mp.remove(A[curr_begin])
        myexactlog(6, mp)
        curr_sum -= B[curr_begin]
        myexactlog(7, curr_sum)
        curr_begin += 1
        myexactlog(8, curr_begin)
        break
    mp.add(A[i])
    myexactlog(9, mp)
    break