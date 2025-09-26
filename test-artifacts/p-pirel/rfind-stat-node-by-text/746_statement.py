while j <= n and curr_sum <= sum_0:
    if curr_sum == sum_0:
        print("Sum found between")
        print("indexes %d and %d" % (i, j - 1))
        return 1
    if j == n:
        break
    curr_sum = curr_sum + arr[j]
    j += 1