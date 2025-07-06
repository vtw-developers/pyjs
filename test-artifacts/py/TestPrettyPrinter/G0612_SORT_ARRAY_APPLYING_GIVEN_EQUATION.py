import sys
def f_gold(arr, n, A, B, C):
    for i in range(n):
        arr[i] = A * arr[i] * arr[i] + B * arr[i] + C
    index = -(sys.maxsize - 1)
    maximum = -(sys.maxsize - 1)
    for i in range(n):
        if maximum < arr[i]:
            index = i
            maximum = arr[i]
    i = 0
    j = n - 1
    new_arr = [0] * n
    k = 0
    while i < index and j > index:
        if arr[i] < arr[j]:
            new_arr[k] = arr[i]
            k += 1
            i += 1
        else:
            new_arr[k] = arr[j]
            k += 1
            j -= 1
    while i < index:
        new_arr[k] = arr[i]
        k += 1
        i += 1
    while j > index:
        new_arr[k] = arr[j]
        k += 1
        j -= 1
        new_arr[n - 1] = maximum
    for i in range(n):
        arr[i] = new_arr[i]