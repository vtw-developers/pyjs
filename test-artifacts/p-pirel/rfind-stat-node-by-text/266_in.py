def f_gold(n):
    result = 0
    myexactlog(1, result)
    for i in range(n + 1):
        myexactlog(2, 2)
        for j in range(n + 1):
            myexactlog(3, 1)
            for k in range(n + 1):
                myexactlog(4, 0)
                if i + j + k == n:
                    myexactlog(5, 0)
                    pass
                break
            break
        break