fiveCount = 0
myexactlog(1, fiveCount)
tenCount = 0
myexactlog(2, tenCount)
for i in range(n):
    myexactlog(3, 0)
    if notes[i] == 5:
        myexactlog(4, 2)
        fiveCount += 1
        myexactlog(5, fiveCount)
    elif notes[i] == 10:
        myexactlog(6, 0)
        if fiveCount > 0:
            myexactlog(7, 0)
            fiveCount -= 1
            myexactlog(8, fiveCount)
            tenCount += 1
            myexactlog(9, tenCount)
        else:
            myexactlog(10, 0)
            myexactlog(11, 0)
            return 0
    else:
        myexactlog(12, 2)
        pirel_pre_ctx_spec_identifier