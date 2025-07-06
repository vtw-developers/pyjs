def f_gold(arr, n):
    count = 0
    cummulative_sum = 0
    arr.sort()
    for i in range(n):
        if arr[i] >= cummulative_sum:
            count += 1
            cummulative_sum += arr[i]
    return count