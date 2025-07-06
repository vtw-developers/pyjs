def f_gold(arr, n):
    max_ele = arr[n - 1]
    min_ele = arr[0]
    for i in range(n):
        if i % 2 == 0:
            arr[i] = max_ele
            max_ele -= 1
        else:
            arr[i] = min_ele
            min_ele += 1