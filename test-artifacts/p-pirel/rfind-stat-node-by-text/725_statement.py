for l in range(1, n):
    myexactlog(7, 0)
    ugly[l] = min(next_multiple_of_2, next_multiple_of_3, next_multiple_of_5)
    myexactlog(8, ugly)
    if ugly[l] == next_multiple_of_2:
        myexactlog(9, 0)
        pass
    break