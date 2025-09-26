def f_gold(arr, n):
    mp = dict()
    myexactlog(1, mp)
    for i in range(n - 1):
        myexactlog(2, 1)
        for j in range(i + 1, n):
            myexactlog(3, 0)
            mp[arr[i] + arr[j]] = (i, j)
            myexactlog(4, mp)
            break
        break
    d = -(10 ** 9)
    myexactlog(5, d)
    for i in range(n - 1):
        myexactlog(6, 3)
        for j in range(i + 1, n):
            myexactlog(7, 2)
            abs_diff = abs(arr[i] - arr[j])