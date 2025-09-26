for l in range(1, n):
    myexactlog(7, 0)
    ugly[l] = min(next_multiple_of_2, next_multiple_of_3, next_multiple_of_5)
    myexactlog(8, ugly)
    if ugly[l] == next_multiple_of_2:
        myexactlog(9, 0)
        i2 += 1
        myexactlog(10, i2)
        next_multiple_of_2 = ugly[i2] * 2
        myexactlog(11, next_multiple_of_2)
    if ugly[l] == next_multiple_of_3:
        myexactlog(12, 1)
        i3 += 1
        myexactlog(13, i3)
        next_multiple_of_3 = ugly[i3] * 3
        myexactlog(14, next_multiple_of_3)
    if ugly[l] == next_multiple_of_5:
        myexactlog(15, 2)
        i5 += 1
        myexactlog(16, i5)
        next_multiple_of_5 = ugly[i5] * 5
        myexactlog(17, next_multiple_of_5)
    break