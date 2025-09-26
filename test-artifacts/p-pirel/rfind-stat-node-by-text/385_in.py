def f_gold(Str):
    Len = len(Str)
    myexactlog(1, Len)
    res = [None] * Len
    myexactlog(2, res)
    index = 0
    myexactlog(3, index)
    i = 0
    myexactlog(4, i)
    s = []
    myexactlog(5, s)
    s.append(0)
    myexactlog(6, s)
    while i < Len:
        myexactlog(7, 0)
        if Str[i] == "+":
            myexactlog(8, 0)
            pass
        elif Str[i] == "-":
            myexactlog(9, 0)
            pass
        elif Str[i] == "(":
            myexactlog(10, 1)
            pass
        elif Str[i] == ")":
            myexactlog(11, 2)
            pass
        else:
            myexactlog(12, 0)
            pass
        break