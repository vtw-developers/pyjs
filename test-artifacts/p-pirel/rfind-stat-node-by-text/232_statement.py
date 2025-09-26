while 1:
    myexactlog(10, 0)
    if top1 == n1 or top2 == n2 or top3 == n3:
        myexactlog(11, 0)
        myexactlog(12, 0)
        return 0
    if sum1 == sum2 and sum2 == sum3:
        myexactlog(13, 1)
        pass
    break