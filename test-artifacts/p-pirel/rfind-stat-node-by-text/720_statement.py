for i in range(size):
    if dict_0[arr[i]] > 1:
        continue
    else:
        KthIndex = KthIndex - 1
    if KthIndex == 0:
        retval_1 = arr[i]
        return retval_1