def f_gold(arr, n):
    msis = [None] * n
    msds = [None] * n
    max_sum = 0
    msis[0] = arr[0]
    for i in range(1, n):
        if arr[i] > arr[i - 1]:
            msis[i] = msis[i - 1] + arr[i]
        else:
            msis[i] = arr[i]
    msds[n - 1] = arr[n - 1]
    for i in range(n - 2, -1, -1):
        if arr[i] > arr[i + 1]:
            msds[i] = msds[i + 1] + arr[i]
        else:
            msds[i] = arr[i]
    for i in range(n):
        if max_sum < (msis[i] + msds[i] - arr[i]):
            max_sum = msis[i] + msds[i] - arr[i]
    return max_sum