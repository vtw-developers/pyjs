if x <= arr[low]:
    return low
if x > arr[high]:
    return -1
mid = (low + high) // 2
if arr[mid] == x:
    return mid
elif arr[mid] < x:
    if mid + 1 <= high and x <= arr[mid + 1]:
        return mid + 1
    else:
        pirel_pre_ctx_spec_identifier
else:
    pass