'\n    :type haystack: str\n    :type needle: str\n    :rtype: int\n    '
for i in range(len(haystack) - len(needle) + 1):
    p = i
    q = 0
    while p < len(haystack) and q < len(needle) and (haystack[p] == needle[q]):
        p += 1
        q += 1
    if q == len(needle):
        return i
return -1