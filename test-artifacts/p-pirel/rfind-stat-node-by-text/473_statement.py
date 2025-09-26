while 1:
    myexactlog(10, 0)
    if top1 == n1 or top2 == n2 or top3 == n3:
        myexactlog(11, 0)
        myexactlog(12, 0)
        return 0
    if sum1 == sum2 and sum2 == sum3:
        myexactlog(13, 1)
        myexactlog(14, sum1)
        return sum1
    if sum1 >= sum2 and sum1 >= sum3:
        myexactlog(15, 2)
        sum1 -= stack1[top1]
        myexactlog(16, sum1)
        top1 = top1 + 1
        myexactlog(17, top1)
    elif sum2 >= sum3 and sum2 >= sum3:
        myexactlog(18, 0)
        sum2 -= stack2[top2]
        myexactlog(19, sum2)
    else:
        myexactlog(20, 0)
        pass
    break