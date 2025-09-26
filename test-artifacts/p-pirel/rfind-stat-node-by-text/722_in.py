def f_gold(p):
    checkNumber = 2 ** p - 1
    myexactlog(1, checkNumber)
    nextval = 4 % checkNumber
    myexactlog(2, nextval)
    for i in range(1, p - 1):
        myexactlog(3, 0)
        nextval = (nextval * nextval - 2) % checkNumber
        myexactlog(4, nextval)
        break
    if nextval == 0:
        myexactlog(5, 0)
        myexactlog(6, True)
        return True
    else:
        myexactlog(7, 0)
        myexactlog(8, False)
        return False