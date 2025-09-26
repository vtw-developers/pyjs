for i in range(1, n):
    myexactlog(7, 3)
    currHam = 0
    myexactlog(8, currHam)
    k = 0
    myexactlog(9, k)
    for j in range(i, i + n):
        myexactlog(10, 2)
        if brr[j] != arr[k]:
            myexactlog(11, 0)
            currHam += 1
            myexactlog(12, currHam)
        break
    break