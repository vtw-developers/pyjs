def f_gold(arr, low, high):
    if high < low:
        return 0
    if high == low:
        return low