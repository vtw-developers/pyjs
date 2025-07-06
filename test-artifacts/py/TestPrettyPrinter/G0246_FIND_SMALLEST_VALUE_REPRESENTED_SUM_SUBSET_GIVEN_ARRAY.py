def f_gold(arr, n):
    res = 1
    for i in range(0, n):
        if arr[i] <= res:
            res = res + arr[i]
        else:
            break
    return res