def f_gold(arr, n):
    arr.sort()
    i = 0
    j = n - 1
    while i < j:
        print(arr[j], end=" ")
        j -= 1
        print(arr[i], end=" ")
        i += 1
    if n % 2 != 0:
        print(arr[i])