def f_gold(arr, n, sum):
    curr_sum = arr[0]
    start = 0
    i = 1
    while i <= n:
        while curr_sum > sum and start < i - 1:
            curr_sum = curr_sum - arr[start]
            start += 1
        if curr_sum == sum:
            print("Sum found between indexes")
            print("%d and %d" % (start, i - 1))
            return 1
        if i < n:
            curr_sum = curr_sum + arr[i]
        i += 1
    print("No subarray found")
    return 0