def f_gold(arr, n):
    mpis = [0] * (n)
    for i in range(n):
        mpis[i] = arr[i]
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and mpis[i] < (mpis[j] * arr[i]):
                mpis[i] = mpis[j] * arr[i]
    return max(mpis)