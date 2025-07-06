def f_gold(arr, n, x):
    if n < 2:
        return False
    s = set()
    for i in range(0, n):
        if arr[i] == 0:
            if x == 0:
                return True
            else:
                continue
        if x % arr[i] == 0:
            if x // arr[i] in s:
                return True
            s.add(arr[i])
    return False