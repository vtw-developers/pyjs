def f_gold(arr, l, r, x):
    if r < l:
        return -1
    if arr[l] == x:
        return l
    if arr[r] == x:
        return r
    return f_gold(arr, l + 1, r - 1, x)