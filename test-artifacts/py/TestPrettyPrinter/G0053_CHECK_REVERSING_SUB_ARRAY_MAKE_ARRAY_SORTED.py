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
    if front >= back:
        return True
    while front != back:
        front += 1
        if arr[front - 1] < arr[front]:
            return False
    return True