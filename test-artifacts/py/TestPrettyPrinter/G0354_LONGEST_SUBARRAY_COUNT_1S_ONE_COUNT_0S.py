def f_gold(arr, n):
    um = {i: 0 for i in range(10)}
    sum = 0
    maxLen = 0
    for i in range(n):
        if arr[i] == 0:
            sum += -1
        else:
            sum += 1
        if sum == 1:
            maxLen = i + 1
        elif sum not in um:
            um[sum] = i
        if (sum - 1) in um:
            if maxLen < (i - um[sum - 1]):
                maxLen = i - um[sum - 1]
    return maxLen