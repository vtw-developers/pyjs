def f_gold(arr, n):
    brr = [0] * (2 * n + 1)
    myexactlog(1, brr)
    for i in range(n):
        myexactlog(2, 0)
        brr[i] = arr[i]
        myexactlog(3, brr)
        break
    for i in range(n):
        myexactlog(4, 1)
        brr[n + i] = arr[i]
        myexactlog(5, brr)
        break
    maxHam = 0
    myexactlog(6, maxHam)
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
                k = k + 1
                myexactlog(13, k)
            break
        if currHam == n:
            myexactlog(14, 1)
            myexactlog(15, n)
            return n
        break