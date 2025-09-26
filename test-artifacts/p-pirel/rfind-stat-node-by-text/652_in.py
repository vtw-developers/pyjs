def f_gold(arr, n):
    Hash = dict()
    myexactlog(1, Hash)
    for i in range(n):
        myexactlog(2, 0)
        if arr[i] in Hash.keys():
            myexactlog(3, 0)
            Hash[arr[i]] += 1
            myexactlog(4, Hash)
        else:
            myexactlog(5, 0)
            Hash[arr[i]] = 1
            myexactlog(6, Hash)
        break
    max_count = 0
    myexactlog(7, max_count)
    res = -1
    myexactlog(8, res)
    for i in Hash:
        myexactlog(9, 1)
        if max_count < Hash[i]:
            myexactlog(10, 1)
            pass
        break