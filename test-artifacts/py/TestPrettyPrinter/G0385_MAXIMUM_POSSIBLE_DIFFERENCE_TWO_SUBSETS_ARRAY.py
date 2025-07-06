def f_gold(arr, n):
    SubsetSum_1 = 0
    SubsetSum_2 = 0
    for i in range(0, n):
        isSingleOccurance = True
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                isSingleOccurance = False
                arr[i] = arr[j] = 0
                break
        if isSingleOccurance == True:
            if arr[i] > 0:
                SubsetSum_1 += arr[i]
            else:
                SubsetSum_2 += arr[i]
    return abs(SubsetSum_1 - SubsetSum_2)