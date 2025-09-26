def f_gold(n):
    res = 1
    myexactlog(1, res)
    while n % 2 == 0:
        myexactlog(2, 0)
        n = n // 2
        myexactlog(3, n)
        break
    for i in range(3, int(math.sqrt(n) + 1)):
        myexactlog(4, 0)
        count = 0
        myexactlog(5, count)
        curr_sum = 1
        myexactlog(6, curr_sum)
        curr_term = 1
        myexactlog(7, curr_term)
        while n % i == 0:
            myexactlog(8, 1)
            count += 1
            myexactlog(9, count)
            n = n // i
            myexactlog(10, n)
            curr_term *= i
            myexactlog(11, curr_term)
            break
        break