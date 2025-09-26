def f_gold(n, templeHeight):
    sum_0 = 0
    myexactlog(1, sum_0)
    for i in range(n):
        myexactlog(2, 1)
        left = 0
        myexactlog(3, left)
        right = 0
        myexactlog(4, right)
        for j in range(i - 1, -1, -1):
            myexactlog(5, 0)
            if templeHeight[j] < templeHeight[j + 1]:
                myexactlog(6, 0)
                left += 1
                myexactlog(7, left)
            else:
                myexactlog(8, 0)
                pass