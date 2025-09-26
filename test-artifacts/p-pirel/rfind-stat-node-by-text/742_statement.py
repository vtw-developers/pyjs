if len(str1) > len(str2):
    myexactlog(1, 0)
    t = str1
    myexactlog(2, t)
    str1 = str2
    myexactlog(3, str1)
    str2 = t
    myexactlog(4, str2)