def f_gold(arr, n):
    s = []
    first = 0
    second = 0
    for i in range(n):
        if arr[i] not in s:
            s.append(arr[i])
            continue
        if arr[i] > first:
            second = first
            first = arr[i]
        elif arr[i] > second:
            second = arr[i]
    return first * second