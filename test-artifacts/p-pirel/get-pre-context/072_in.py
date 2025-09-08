def f_gold(notes, n):
    fiveCount = 0
    myexactlog(1, fiveCount)
    tenCount = 0
    myexactlog(2, tenCount)
    for i in range(n):
        myexactlog(3, 0)
        if notes[i] == 5:
            myexactlog(4, 1)
            fiveCount += 1
            myexactlog(5, fiveCount)
        elif notes[i] == 10:
            myexactlog(6, 0)
            if fiveCount > 0:
                myexactlog(7, 0)
                pass
            else:
                myexactlog(8, 0)
                pass
        else:
            myexactlog(9, 1)
            pass
        break