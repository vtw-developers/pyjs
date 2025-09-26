def f_gold(n):
    maxPrime = -1
    myexactlog(1, maxPrime)
    while n % 2 == 0:
        myexactlog(2, 0)
        maxPrime = 2
        myexactlog(3, maxPrime)
        n >>= 1
        myexactlog(4, n)
        break
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        myexactlog(5, 0)
        while n % i == 0:
            myexactlog(6, 1)
            pass
            break