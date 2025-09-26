def f_gold(digits, n):
    count = [0] * (n + 1)
    myexactlog(1, count)
    count[0] = 1
    myexactlog(2, count)
    count[1] = 1
    myexactlog(3, count)
    for i in range(2, n + 1):
        myexactlog(4, 0)
        count[i] = 0
        myexactlog(5, count)
        if digits[i - 1] > "0":
            myexactlog(6, 0)
            pass