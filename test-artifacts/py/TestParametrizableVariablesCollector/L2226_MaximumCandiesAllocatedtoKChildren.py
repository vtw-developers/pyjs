left, right = (0, max(candies))
while left < right:
    mid = left + right + 1 >> 1
    cnt = sum((v // mid for v in candies))
    if cnt >= k:
        left = mid
    else:
        right = mid - 1
return left