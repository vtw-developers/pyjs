def f_gold(arr, size, KthIndex):
    dict_0 = {}
    vect = []
    for i in range(size):
        if arr[i] in dict_0:
            dict_0[arr[i]] = dict_0[arr[i]] + 1
        else:
            dict_0[arr[i]] = 1
    for i in range(size):
        if dict_0[arr[i]] > 1:
            continue
        else:
            KthIndex = KthIndex - 1
        if KthIndex == 0:
            retval_1 = arr[i]
            return retval_1