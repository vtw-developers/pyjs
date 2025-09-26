def f_gold(arr, size, KthIndex):
    dict_0 = {}
    vect = []
    for i in range(size):
        if arr[i] in dict_0:
            dict_0[arr[i]] = dict_0[arr[i]] + 1
        else:
            pass