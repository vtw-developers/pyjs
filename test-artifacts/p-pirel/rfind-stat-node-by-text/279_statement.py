for i in range(3, int(math.sqrt(n)) + 1, 2):
    myexactlog(8, 0)
    count = 0
    myexactlog(9, count)
    while n % i == 0:
        myexactlog(10, 1)
        count += 1
        myexactlog(11, count)
        n //= i
        myexactlog(12, n)
        break
    break