def f_gold(n):
    count = 0
    myexactlog(1, count)
    for i in range(0, n + 1):
        myexactlog(2, 2)
        for j in range(0, n + 1):
            myexactlog(3, 1)
            for k in range(0, n + 1):
                myexactlog(4, 0)
                if i + j + k == n:
                    myexactlog(5, 0)
                    count = count + 1
                    myexactlog(6, count)
    myexactlog(7, count)
    return count