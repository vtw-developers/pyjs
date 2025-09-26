def f_gold(arr1, n, arr2, m):
    table = [0] * m
    for j in range(m):
        table[j] = 0
    for i in range(n):
        current = 0
        for j in range(m):
            if arr1[i] == arr2[j]:
                if current + 1 > table[j]:
                    table[j] = current + 1
            if arr1[i] > arr2[j]:
                if table[j] > current:
                    current = table[j]
    result = 0
    for i in range(m):
        if table[i] > result:
            result = table[i]