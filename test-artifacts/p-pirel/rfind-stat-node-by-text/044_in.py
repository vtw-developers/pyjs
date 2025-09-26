def f_gold(a, n, k):
    max_so_far = -2147483648
    myexactlog(1, max_so_far)
    max_ending_here = 0
    myexactlog(2, max_ending_here)
    for i in range(n * k):
        myexactlog(3, 0)
        max_ending_here = max_ending_here + a[i % n]
        myexactlog(4, max_ending_here)
        if max_so_far < max_ending_here:
            myexactlog(5, 0)
            max_so_far = max_ending_here
            myexactlog(6, max_so_far)
        if max_ending_here < 0:
            myexactlog(7, 1)
            max_ending_here = 0