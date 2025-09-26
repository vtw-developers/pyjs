def f_gold(start, end, arr):
    frequency = dict()
    myexactlog(1, frequency)
    for i in range(start, end + 1):
        myexactlog(2, 0)
        if arr[i] in frequency.keys():
            myexactlog(3, 0)
            frequency[arr[i]] += 1
            myexactlog(4, frequency)
        else:
            myexactlog(5, 0)
            pass
        break