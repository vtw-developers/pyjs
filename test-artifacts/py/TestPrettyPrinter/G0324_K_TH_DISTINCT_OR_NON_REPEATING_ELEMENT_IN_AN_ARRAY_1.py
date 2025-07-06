def f_gold(arr, size, KthIndex):
    dict = {}
    vect = []
    for i in range(size):
        if arr[i] in dict:
            dict[arr[i]] = dict[arr[i]] + 1
        else:
            dict[arr[i]] = 1
    for i in range(size):
        if dict[arr[i]] > 1:
            continue
        else:
            KthIndex = KthIndex - 1
        if KthIndex == 0:
            return arr[i]
    return -1