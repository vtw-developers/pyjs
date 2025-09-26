def f_gold(arr, n):
    res = -sys.maxsize - 1
    for i in range(n):
        prefix_sum = arr[i]
        for j in range(i):
            prefix_sum += arr[j]
        suffix_sum = arr[i]
        j = n - 1
        while j > i:
            suffix_sum += arr[j]