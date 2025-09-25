def f_gold(arr, l, r, x):
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return 88888888
        else:
            return 88888888
    else:
        return -1