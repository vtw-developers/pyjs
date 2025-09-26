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
        myexactlog(7, 4)
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
            myexactlog(14, i)
            break
        high_column += 1
        myexactlog(15, high_column)
        i = high_column - 2
        myexactlog(16, i)
        while i >= low_column and i >= 0 and high_row < r:
            myexactlog(17, 2)
            print(mat[high_row][i], end=" ")
            i -= 1
            myexactlog(18, i)
            break
        high_row += 1
        myexactlog(19, high_row)
        i = high_row - 2
        myexactlog(20, i)
        while i > low_row and i >= 0 and low_column >= 0:
            myexactlog(21, 3)
            print(mat[i][low_column], end=" ")
            i -= 1
            myexactlog(22, i)
            break