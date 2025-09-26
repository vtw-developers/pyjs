def f_gold(n):
    count = 0
    myexactlog(1, count)
    ans = 1
    myexactlog(2, ans)
    while n % 2 == 0:
        myexactlog(3, 0)
        count += 1
        myexactlog(4, count)
        n //= 2
        myexactlog(5, n)
        break
    if count % 2 != 0:
        myexactlog(6, 0)
        ans *= 2
        myexactlog(7, ans)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        myexactlog(8, 0)
        count = 0
        myexactlog(9, count)
        while n % i == 0:
            myexactlog(10, 1)
            count += 1