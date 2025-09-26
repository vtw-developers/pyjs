while n % i == 0:
    myexactlog(8, 1)
    count += 1
    myexactlog(9, count)
    n = n // i
    myexactlog(10, n)
    curr_term *= i
    myexactlog(11, curr_term)
    curr_sum += curr_term
    myexactlog(12, curr_sum)
    break