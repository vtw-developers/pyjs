def f_gold(arr, size):
    Hash = dict()
    for i in range(size):
        Hash[arr[i]] = Hash.get(arr[i], 0) + 1
    for i in Hash:
        if Hash[i] % 2 != 0:
            return i
    return -1