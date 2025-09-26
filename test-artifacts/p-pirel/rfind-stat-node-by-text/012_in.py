def f_gold(arr, n):
    ans = -float("inf")
    maxval = 1
    minval = 1
    for i in range(0, n):
        if arr[i] > 0:
            maxval = maxval * arr[i]
        elif arr[i] == 0:
            pass
        else:
            pass