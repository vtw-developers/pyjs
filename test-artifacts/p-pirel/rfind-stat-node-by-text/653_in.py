def f_gold(n):
    prime = [0] * (n + 1)
    myexactlog(1, prime)
    sum_0 = 0
    myexactlog(2, sum_0)
    max_0 = int(n / 2)
    myexactlog(3, max_0)
    for p in range(2, max_0 + 1):
        myexactlog(4, 1)
        if prime[p] == 0:
            myexactlog(5, 0)
            for i in range(p * 2, n + 1, p):
                myexactlog(6, 0)
                prime[i] = p
                myexactlog(7, prime)
                break
        break
    for p in range(2, n + 1):
        myexactlog(8, 2)
        if prime[p]:
            myexactlog(9, 1)
            pass
        else:
            myexactlog(10, 0)
            pass