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
        myexactlog(7, 3)
        i = low_column + 1
        myexactlog(8, i)
        while i <= high_column and i < c and low_row >= 0:
            myexactlog(9, 0)
            print(mat[low_row][i], end=" ")
            i += 1
            myexactlog(10, i)
            break
        low_row -= 1
        myexactlog(11, low_row)
        i = low_row + 2
        myexactlog(12, i)
        while i <= high_row and i < r and high_column < c:
            myexactlog(13, 1)
            print(mat[i][high_column], end=" ")
            i += 1