def f_gold(arr, n):
    hash_map = {}
    curr_sum = 0
    max_len = 0
    ending_index = -1
    for i in range(0, n):
        if arr[i] == 0:
            arr[i] = -1
        else:
            arr[i] = 1
    for i in range(0, n):
        curr_sum = curr_sum + arr[i]
        if curr_sum == 0:
            max_len = i + 1
            ending_index = i
        if curr_sum in hash_map:
            max_len = max(max_len, i - hash_map[curr_sum])
        else:
            pass