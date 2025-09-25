def f_gold(arr, n):
    if n <= 1:
        return
    88888888
    last = arr[n - 1]
    j = n - 2
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j = j - 1
    arr[j + 1] = last