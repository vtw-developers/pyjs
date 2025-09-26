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
            if row == m - 1 or col == n - 1:
                myexactlog(12, 2)
                right_down = 0
                myexactlog(13, right_down)
            else:
                myexactlog(14, 2)
                right_down = goldTable[row + 1][col + 1]
                myexactlog(15, right_down)
            goldTable[row][col] = gold[row][col] + max(right, right_up, right_down)
            myexactlog(16, goldTable)
            break
        break
    res = goldTable[0][0]
    myexactlog(17, res)
    for i in range(1, m):
        myexactlog(18, 2)
        res = max(res, goldTable[i][0])