for i in range(start, end + 1):
    if arr[i] in frequency.keys():
        frequency[arr[i]] += 1
    else:
        frequency[arr[i]] = 1