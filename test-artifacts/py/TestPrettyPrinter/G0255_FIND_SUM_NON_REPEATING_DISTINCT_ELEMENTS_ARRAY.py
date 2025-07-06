def f_gold(arr, n):
    s = set()
    sum = 0
    for i in range(n):
        if arr[i] not in s:
            s.add(arr[i])
    for i in s:
        sum = sum + i
    return sum