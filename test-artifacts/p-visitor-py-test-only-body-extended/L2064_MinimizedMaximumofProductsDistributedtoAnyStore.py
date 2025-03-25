left, right = (1, int(100000.0))
while left < right:
    mid = left + right >> 1
    s = sum([(q + mid - 1) // mid for q in quantities])
    if s <= n:
        right = mid
    else:
        left = mid + 1
return left