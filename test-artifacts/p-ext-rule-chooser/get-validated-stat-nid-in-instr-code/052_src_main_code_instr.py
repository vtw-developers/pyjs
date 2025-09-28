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
        length += 2
        myexactlog(6, length)
    elif length % 3 == 2:
        myexactlog(7, 0)
        num = str(num) + "0"
        myexactlog(8, num)
        length += 1
        myexactlog(9, length)