def f_gold(arr, n, k):
    for i in range(n):
        count = 0
        for j in range(n):
            if arr[j] == arr[i]:
                count += 1
            if count > 2 * k:
                return False
    return True