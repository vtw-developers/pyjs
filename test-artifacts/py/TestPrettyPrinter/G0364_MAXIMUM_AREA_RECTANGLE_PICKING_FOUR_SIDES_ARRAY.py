def f_gold(arr, n):
    arr.sort(reverse=True)
    dimension = [0, 0]
    i = 0
    j = 0
    while i < n - 1 and j < 2:
        if arr[i] == arr[i + 1]:
            dimension[j] = arr[i]
            j += 1
            i += 1
        i += 1
    return dimension[0] * dimension[1]