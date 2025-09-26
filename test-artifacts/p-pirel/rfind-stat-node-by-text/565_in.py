def f_gold(arr, size, KthIndex):
    dict_0 = {}
    myexactlog(1, dict_0)
    vect = []
    myexactlog(2, vect)
    for i in range(size):
        myexactlog(3, 0)
        if arr[i] in dict_0:
            myexactlog(4, 0)
            dict_0[arr[i]] = dict_0[arr[i]] + 1
            myexactlog(5, dict_0)
        else:
            myexactlog(6, 0)
            dict_0[arr[i]] = 1
            myexactlog(7, dict_0)
        break
    for i in range(size):
        myexactlog(8, 1)
        pass
        break