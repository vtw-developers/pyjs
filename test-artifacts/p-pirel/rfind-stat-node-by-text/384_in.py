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
            myexactlog(7, third)
            second = first
            myexactlog(8, second)
            first = arr[i]
            myexactlog(9, first)
        elif arr[i] > second:
            myexactlog(10, 0)
            third = second
            myexactlog(11, third)
        elif arr[i] > third:
            myexactlog(12, 1)
            pass
        break