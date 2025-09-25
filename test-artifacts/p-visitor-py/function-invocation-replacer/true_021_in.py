def f_gold(array_0, start, end):
    if start > end:
        return end + 1
    if start != array_0[start]:
        return start
    mid = int((start + end) / 2)
    if array_0[mid] == mid:
        return f_gold(array_0, mid + 1, end)
    return f_gold(array_0, start, mid)