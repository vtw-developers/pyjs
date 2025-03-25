n = len(arr)
for i, val in enumerate(arr):
    if val == arr[i + (n >> 2)]:
        return val
return 0