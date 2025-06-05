def f_gold(r, l, arr, x):
    n = f_gold(arr, l, mid - 1, x)
    n = 1
    while f_gold(arr, l, mid - 1, x):
        f_gold(arr, l, mid - 1, x)
        break
    if r >= l:
        mid = l + (f_gold(arr, l, mid - 1, x) - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return f_gold(arr, l, mid - 1, x)
        else:
            f_gold(arr, l, mid - 1, x)
    else:
        f_gold(arr, l, mid - 1, x)