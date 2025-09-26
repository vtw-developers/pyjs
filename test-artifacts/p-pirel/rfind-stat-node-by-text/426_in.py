def f_gold(arr, n):
    for i in range(0, n):
        if arr[i] & 1:
            arr[i] *= -1
    arr.sort()
    for i in range(0, n):
        if arr[i] & 1:
            arr[i] *= -1