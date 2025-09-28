def f_gold(str_0):
    zeros = 0
    myexactlog(1, zeros)
    ones = 0
    myexactlog(2, ones)
    for i in range(0, len(str_0)):
        myexactlog(3, 0)
        ch = str_0[i]
        myexactlog(4, ch)
        if ch == "0":
            myexactlog(5, 0)
            zeros = zeros + 1
            myexactlog(6, zeros)
        else:
            myexactlog(7, 0)
            ones = ones + 1
            myexactlog(8, ones)
    retval_1 = zeros == 1 or ones == 1
    myexactlog(9, retval_1)
    myexactlog(10, retval_1)
    return retval_1