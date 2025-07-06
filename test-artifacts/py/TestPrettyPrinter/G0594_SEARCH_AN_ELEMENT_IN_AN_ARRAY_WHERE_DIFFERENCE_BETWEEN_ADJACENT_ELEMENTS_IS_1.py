def f_gold(arr, n, x):
    i = 0
    while i < n:
        if arr[i] == x:
            return i
        i = i + abs(arr[i] - x)
    print("number is not present!")
    return -1