def f_gold(arr, n):
    if n == 1:
        return True
    i = 1
    for i in range(1, n):
        if arr[i - 1] < arr[i]:
            if i == n:
                return True
    j = i
    while arr[j] < arr[j - 1]:
        if i > 1 and arr[j] < arr[i - 2]:
            return False
        j += 1
    if j == n:
        return True
    k = j
    if arr[k] < arr[i - 1]:
        return False
    while k > 1 and k < n:
        if arr[k] < arr[k - 1]:
            return False
        k += 1
    return True