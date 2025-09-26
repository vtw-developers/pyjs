def f_gold(arr, arr_size):
    if arr_size < 3:
        print(" Invalid Input ")
        return
    first = arr[0]
    second = -sys.maxsize
    third = -sys.maxsize
    for i in range(1, arr_size):
        if arr[i] > first:
            third = second
            second = first
            first = arr[i]
        elif arr[i] > second:
            third = second
        elif arr[i] > third:
            pass