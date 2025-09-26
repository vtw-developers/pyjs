def f_gold(arr, n):
    temp = [0] * n
    for i in range(n):
        temp[i] = arr[i]
    temp.sort()
    for front in range(n):
        if temp[front] != arr[front]:
            break
    for back in range(n - 1, -1, -1):
        if temp[back] != arr[back]:
            break