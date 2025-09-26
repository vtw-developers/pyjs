for i in range(0, arr_size):
    myexactlog(11, 2)
    if arr[i] > third and arr[i] < second:
        myexactlog(12, 3)
        third = arr[i]
        myexactlog(13, third)
    break