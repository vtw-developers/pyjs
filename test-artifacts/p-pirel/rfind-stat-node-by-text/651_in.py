def f_gold(n):
    ugly = [0] * n
    myexactlog(1, ugly)
    ugly[0] = 1
    myexactlog(2, ugly)
    i2 = i3 = i5 = 0
    myexactlog(3, i2)
    next_multiple_of_2 = 2
    myexactlog(4, next_multiple_of_2)
    next_multiple_of_3 = 3
    myexactlog(5, next_multiple_of_3)
    next_multiple_of_5 = 5
    myexactlog(6, next_multiple_of_5)
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