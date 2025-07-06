def f_gold(arr, n, k):
    for i in range(k, n):
        max_var = arr[k - 1]
        pos = k - 1
        for j in range(k - 2, -1, -1):
            if arr[j] > max_var:
                max_var = arr[j]
                pos = j
        if max_var > arr[i]:
            j = pos
            while j < k - 1:
                arr[j] = arr[j + 1]
                j += 1
            arr[k - 1] = arr[i]
    for i in range(0, k):
        print(arr[i], end=" ")