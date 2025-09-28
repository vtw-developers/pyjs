def f_gold(num):
    length = len(num)
    myexactlog(1, length)
    if length == 1 and num[0] == "0":
        myexactlog(2, 0)
        myexactlog(3, True)
        return True
    if length % 3 == 1:
        myexactlog(4, 1)
        num = str(num) + "00"
        myexactlog(5, num)
    elif length % 3 == 2:
        myexactlog(6, 0)
        pass