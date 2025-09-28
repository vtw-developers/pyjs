def f_gold(num):
    length = len(num)
    myexactlog(1, length)
    if length == 1 and num[0] == "0":
        myexactlog(2, 0)
        myexactlog(3, True)
        return True