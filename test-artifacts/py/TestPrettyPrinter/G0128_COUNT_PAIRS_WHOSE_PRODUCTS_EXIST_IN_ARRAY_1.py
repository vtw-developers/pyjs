def f_gold(arr, n):
    result = 0
    Hash = set()
    for i in range(n):
        Hash.add(arr[i])
    for i in range(n):
        for j in range(i + 1, n):
            product = arr[i] * arr[j]
            if product in (Hash):
                result += 1
    return result