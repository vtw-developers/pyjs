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
        third = second
        myexactlog(11, third)
        second = arr[i]
        myexactlog(12, second)
    elif arr[i] > third:
        myexactlog(13, 1)
        third = arr[i]
        myexactlog(14, third)
    break