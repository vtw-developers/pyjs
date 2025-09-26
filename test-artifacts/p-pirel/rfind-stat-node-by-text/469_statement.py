while True:
    myexactlog(3, 1)
    sum_0 = 0
    myexactlog(4, sum_0)
    x = curr
    myexactlog(5, x)
    while x > 0:
        myexactlog(6, 0)
        sum_0 = sum_0 + x % 10
        myexactlog(7, sum_0)
        x = int(x / 10)
        myexactlog(8, x)
        break
    if sum_0 == 10:
        myexactlog(9, 0)
        count += 1
        myexactlog(10, count)
    if count == n:
        myexactlog(11, 1)
        myexactlog(12, curr)
        return curr
    curr += 9
    myexactlog(13, curr)
    break