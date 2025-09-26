def f_gold(mat, r, c):
    a = 0
    myexactlog(1, a)
    b = 2
    myexactlog(2, b)
    low_row = 0 if (0 > a) else a
    myexactlog(3, low_row)
    low_column = 0 if (0 > b) else b - 1
    myexactlog(4, low_column)
    high_row = r - 1 if ((a + 1) >= r) else a + 1
    myexactlog(5, high_row)
    high_column = c - 1 if ((b + 1) >= c) else b + 1
    myexactlog(6, high_column)
    while low_row > 0 - r and low_column > 0 - c:
        myexactlog(7, 0)
        i = low_column + 1
        myexactlog(8, i)
        break