def f_gold(arr, n):
    hash_0 = dict()
    myexactlog(1, hash_0)
    maximum = 0
    myexactlog(2, maximum)
    for i in arr:
        myexactlog(3, 0)
        if i < 0:
            myexactlog(4, 1)
            if abs(i) not in hash_0.keys():
                myexactlog(5, 0)
                hash_0[abs(i)] = -1
                myexactlog(6, hash_0)
            else:
                myexactlog(7, 0)
                pass
        else:
            myexactlog(8, 1)
            pass
        break