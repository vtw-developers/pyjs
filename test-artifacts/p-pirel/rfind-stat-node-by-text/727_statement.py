if row == 0 or col == n - 1:
    myexactlog(8, 1)
    right_up = 0
    myexactlog(9, right_up)
else:
    myexactlog(10, 1)
    right_up = goldTable[row - 1][col + 1]
    myexactlog(11, right_up)