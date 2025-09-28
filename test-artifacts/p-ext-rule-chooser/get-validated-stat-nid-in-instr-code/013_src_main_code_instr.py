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
        i -= 1
        myexactlog(9, i)
    num1 = "".join(num)
    myexactlog(10, num1)
    if i < 0:
        myexactlog(11, 1)
        num1 = "1" + num1
        myexactlog(12, num1)
    myexactlog(13, num1)
    return num1