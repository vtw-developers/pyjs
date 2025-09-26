def f_gold(arr, n):
    ans = -float("inf")
    maxval = 1
    minval = 1
    for i in range(0, n):
        if arr[i] > 0:
            maxval = maxval * arr[i]
            minval = min(1, minval * arr[i])
        elif arr[i] == 0:
            minval = 1
            maxval = 0
        else:
            prevMax = maxval
            maxval = minval * arr[i]
            minval = prevMax * arr[i]
        ans = max(ans, maxval)
        if maxval <= 0:
            maxval = 1