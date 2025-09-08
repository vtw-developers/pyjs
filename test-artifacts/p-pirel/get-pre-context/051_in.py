def f_gold(arr, n):
    s = set()
    sum_0 = 0
    for i in range(n):
        sum_0 += arr[i]
    if sum_0 % 2 != 0:
        return False
    sum_0 = sum_0 / 2
    for i in range(n):
        val = sum_0 - arr[i]
        if arr[i] not in s:
            s.add(arr[i])
        if val in s:
            print("Pair elements are", arr[i], "and", int(val))