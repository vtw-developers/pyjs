def f_gold(arr, n, k):
    if k > n:
        return -1
    sum = arr[0]
    for i in range(1, k):
        sum += arr[i]
    max_sum = sum
    max_end = k - 1
    for i in range(k, n):
        sum = sum + arr[i] - arr[i - k]
        if sum > max_sum:
            max_sum = sum
            max_end = i
    return max_end - k + 1