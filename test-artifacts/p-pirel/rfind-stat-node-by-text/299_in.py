def f_gold(n):
    if n % 2 != 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    res = 1
    myexactlog(3, res)
    for i in range(2, int(math.sqrt(n)) + 1):
        myexactlog(4, 0)
        count = 0
        myexactlog(5, count)
        curr_sum = 1
        myexactlog(6, curr_sum)
        curr_term = 1
        myexactlog(7, curr_term)
        while n % i == 0:
            myexactlog(8, 0)
            count = count + 1
            myexactlog(9, count)
            n = n // i
            myexactlog(10, n)
            if i == 2 and count == 1:
                myexactlog(11, 1)
                curr_sum = 0
                myexactlog(12, curr_sum)
            curr_term = curr_term * i
            myexactlog(13, curr_term)
            break