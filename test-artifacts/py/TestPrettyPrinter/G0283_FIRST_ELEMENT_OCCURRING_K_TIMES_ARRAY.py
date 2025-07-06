def f_gold(arr, n, k):
    count_map = {}
    for i in range(0, n):
        if arr[i] in count_map.keys():
            count_map[arr[i]] += 1
        else:
            count_map[arr[i]] = 1
        i += 1
    for i in range(0, n):
        if count_map[arr[i]] == k:
            return arr[i]
        i += 1
    return -1