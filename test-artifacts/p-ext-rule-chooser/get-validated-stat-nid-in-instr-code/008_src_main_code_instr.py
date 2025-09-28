def f_gold(num1):
    l = len(num1)
    myexactlog(1, l)
    num = list(num1)
    myexactlog(2, num)
    i = l - 1
    myexactlog(3, i)
    while i >= 0:
        myexactlog(4, 0)
        if num[i] == "0":
            myexactlog(5, 0)
            num[i] = "1"
            myexactlog(6, num)
            break
        else:
            myexactlog(7, 0)
            num[i] = "0"
            myexactlog(8, num)
        break