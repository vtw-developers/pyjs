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