def f_gold(a, n):
    a = sorted(a)
    myexactlog(1, a)
    num1, num2 = 0, 0
    myexactlog(2, num1, num2)
    for i in range(n):
        myexactlog(3, 0)
        if i % 2 == 0:
            myexactlog(4, 0)
            num1 = num1 * 10 + a[i]
            myexactlog(5, num1)
        else:
            myexactlog(6, 0)
            num2 = num2 * 10 + a[i]
            myexactlog(7, num2)
        break