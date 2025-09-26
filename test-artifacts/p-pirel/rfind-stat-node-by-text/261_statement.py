for i in range(1, n):
    myexactlog(14, 1)
    if num[i] != "0":
        myexactlog(15, 2)
        if small == -1:
            myexactlog(16, 1)
            pass
        elif num[i] < num[small]:
            myexactlog(17, 0)
            pass
    break