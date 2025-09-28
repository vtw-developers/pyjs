def f_gold(num):
    l = len(num)
    myexactlog(1, l)
    count_zero = 0
    myexactlog(2, count_zero)
    i = 1
    myexactlog(3, i)
    while i < l:
        myexactlog(4, 0)
        ch = num[i]
        myexactlog(5, ch)
        if ch == "0":
            myexactlog(6, 0)
            count_zero = count_zero + 1
            myexactlog(7, count_zero)
        i = i + 1
        myexactlog(8, i)
    myexactlog(9, count_zero)
    return count_zero