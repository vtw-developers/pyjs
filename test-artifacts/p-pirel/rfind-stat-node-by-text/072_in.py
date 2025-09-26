def f_gold(arr, arr_size):
    if arr_size < 3:
        myexactlog(1, 0)
        print(" Invalid Input ")
        return
    first = arr[0]
    myexactlog(2, first)
    second = -sys.maxsize
    myexactlog(3, second)
    third = -sys.maxsize
    myexactlog(4, third)
    for i in range(1, arr_size):
        myexactlog(5, 0)
        if arr[i] > first:
            myexactlog(6, 1)
            third = second
        elif arr[i] > second:
            pass
        elif arr[i] > third:
            pass