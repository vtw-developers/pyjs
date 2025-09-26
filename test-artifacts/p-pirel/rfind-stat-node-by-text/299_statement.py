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