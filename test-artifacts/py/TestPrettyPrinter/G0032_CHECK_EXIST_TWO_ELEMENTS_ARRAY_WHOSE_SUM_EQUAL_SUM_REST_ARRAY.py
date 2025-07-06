def f_gold(arr, n):
    s = set()
    sum = 0
    for i in range(n):
        sum += arr[i]
    if sum % 2 != 0:
        return False
    sum = sum / 2
    for i in range(n):
        val = sum - arr[i]
        if arr[i] not in s:
            s.add(arr[i])
        if val in s:
            print("Pair elements are", arr[i], "and", int(val))