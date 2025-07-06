def f_gold(arr, n):
    max_idx = n - 1
    min_idx = 0
    max_elem = arr[n - 1] + 1
    for i in range(0, n):
        if i % 2 == 0:
            arr[i] += (arr[max_idx] % max_elem) * max_elem
            max_idx -= 1
        else:
            arr[i] += (arr[min_idx] % max_elem) * max_elem
            min_idx += 1
    for i in range(0, n):
        arr[i] = arr[i] / max_elem