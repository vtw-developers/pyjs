left, right = (0, len(letters))
while left < right:
    mid = left + right >> 1
    if ord(letters[mid]) > ord(target):
        right = mid
    else:
        left = mid + 1
return letters[left % len(letters)]