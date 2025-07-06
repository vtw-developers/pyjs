def f_gold(arr, n, sum):
    for i in range(n):
        curr_sum = arr[i]
        j = i + 1
        while j <= n:
            if curr_sum == sum:
                print("Sum found between")
                print("indexes %d and %d" % (i, j - 1))
                return 1
            if curr_sum > sum or j == n:
                break
            curr_sum = curr_sum + arr[j]
            j += 1
    print("No subarray found")
    return 0