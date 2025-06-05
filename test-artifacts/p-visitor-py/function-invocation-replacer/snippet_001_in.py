def f_gold(r, l, arr, x):
    n = 0
    n = 1
    while n < 10:
        n += 1
        break
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return f_gold(arr, l, mid - 1, x)
        else:
            pass
    else:
        pass