def f_gold(gold, m, n):
    goldTable = [[0 for i in range(n)] for j in range(m)]
    myexactlog(1, goldTable)
    for col in range(n - 1, -1, -1):
        myexactlog(2, 1)
        for row in range(m):
            myexactlog(3, 0)
            if col == n - 1:
                myexactlog(4, 0)
                right = 0
                myexactlog(5, right)
            else:
                myexactlog(6, 0)
                right = goldTable[row][col + 1]
                myexactlog(7, right)
            if row == 0 or col == n - 1:
                myexactlog(8, 1)
                right_up = 0
                myexactlog(9, right_up)
            else:
                myexactlog(10, 1)
                right_up = goldTable[row - 1][col + 1]
                myexactlog(11, right_up)