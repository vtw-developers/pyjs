def f_gold(arr, n):
    mp = dict()
    myexactlog(1, mp)
    Sum = 0
    myexactlog(2, Sum)
    count = 0
    myexactlog(3, count)
    for i in range(n):
        myexactlog(4, 0)
        if arr[i] == 0:
            myexactlog(5, 0)
            arr[i] = -1
            myexactlog(6, arr)
        Sum += arr[i]
        myexactlog(7, Sum)
        if Sum == 0:
            myexactlog(8, 1)
            count += 1
            myexactlog(9, count)
        if Sum in mp.keys():
            myexactlog(10, 2)
            count += mp[Sum]
            myexactlog(11, count)
        mp[Sum] = mp.get(Sum, 0) + 1
        myexactlog(12, mp)
        break