def f_gold(str1, str2, k):
    if (len(str1) + len(str2)) < k:
        myexactlog(1, 0)
        myexactlog(2, True)
        return True
    commonLength = 0
    myexactlog(3, commonLength)
    for i in range(0, min(len(str1), len(str2)), 1):
        myexactlog(4, 0)
        if str1[i] == str2[i]:
            myexactlog(5, 1)
            commonLength += 1
            myexactlog(6, commonLength)
        else:
            myexactlog(7, 0)
            break
        break