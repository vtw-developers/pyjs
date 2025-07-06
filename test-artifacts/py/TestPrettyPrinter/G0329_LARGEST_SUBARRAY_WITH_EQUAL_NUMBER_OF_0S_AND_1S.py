def f_gold(arr, n):
    sum = 0
    maxsize = -1
    for i in range(0, n - 1):
        sum = -1 if (arr[i] == 0) else 1
        for j in range(i + 1, n):
            sum = sum + (-1) if (arr[j] == 0) else sum + 1
            if sum == 0 and maxsize < j - i + 1:
                maxsize = j - i + 1
                startindex = i
    if maxsize == -1:
        print("No such subarray")
    else:
        print(startindex, "to", startindex + maxsize - 1)
    return maxsize