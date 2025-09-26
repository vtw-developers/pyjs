for i in range(0, row):
    myexactlog(1, 1)
    for j in range(0, column):
        myexactlog(2, 0)
        if i == j:
            myexactlog(3, 0)
            pass
        break
    break