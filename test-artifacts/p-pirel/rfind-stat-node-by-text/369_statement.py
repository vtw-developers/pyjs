for i in range(1, arr_size):
    myexactlog(5, 0)
    if arr[i] > first:
        myexactlog(6, 1)
        third = second
        myexactlog(7, third)
        second = first
        myexactlog(8, second)
        first = arr[i]
        myexactlog(9, first)
    elif arr[i] > second:
        myexactlog(10, 0)
        pass
    elif arr[i] > third:
        myexactlog(11, 1)
        pass
    break