while i < Len:
    myexactlog(7, 0)
    if Str[i] == "+":
        myexactlog(8, 1)
        if s[-1] == 1:
            myexactlog(9, 0)
            pass
    elif Str[i] == "-":
        myexactlog(10, 0)
        pass
    elif Str[i] == "(":
        myexactlog(11, 1)
        pass
    elif Str[i] == ")":
        myexactlog(12, 2)
        pass
    else:
        myexactlog(13, 0)
        pass
    break