def f_gold(arr, arr_size):
    if arr_size < 3:
        myexactlog(1, 0)
        print(" Invalid Input ")
        return
    first = arr[0]
    myexactlog(2, first)
    for i in range(1, arr_size):
        myexactlog(3, 0)
        if arr[i] > first:
            myexactlog(4, 1)
            first = arr[i]
            myexactlog(5, first)
        break
    second = -sys.maxsize
    myexactlog(6, second)
    for i in range(0, arr_size):
        myexactlog(7, 1)
        if arr[i] > second and arr[i] < first:
            myexactlog(8, 2)
            second = arr[i]
            myexactlog(9, second)
        break
    third = -sys.maxsize
    myexactlog(10, third)
    for i in range(0, arr_size):
        myexactlog(11, 2)
        if arr[i] > third and arr[i] < second:
            myexactlog(12, 3)
            third = arr[i]
            myexactlog(13, third)
        break