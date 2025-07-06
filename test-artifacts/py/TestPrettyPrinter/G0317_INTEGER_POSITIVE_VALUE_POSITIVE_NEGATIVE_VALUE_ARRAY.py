def f_gold(arr, n):
    hash = dict()
    maximum = 0
    for i in arr:
        if i < 0:
            if abs(i) not in hash.keys():
                hash[abs(i)] = -1
            else:
                hash[abs(i)] -= 1
        else:
            hash[i] = hash.get(i, 0) + 1
    for i in arr:
        if i in hash.keys() and hash[i] > 0:
            return i
    return -1