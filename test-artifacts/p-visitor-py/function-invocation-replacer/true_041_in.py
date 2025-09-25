def f_gold(arr, l, h):
    if l >= h:
        return
    if arr[l] > arr[h]:
        t = arr[l]
        arr[l] = arr[h]
        arr[h] = t
    if h - l + 1 > 2:
        t = int((h - l + 1) / 3)
        f_gold(arr, l, (h - t))
        f_gold(arr, l + t, (h))
        f_gold(arr, l, (h - t))