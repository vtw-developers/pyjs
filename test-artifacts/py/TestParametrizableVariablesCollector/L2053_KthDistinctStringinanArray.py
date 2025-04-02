counter = Counter(arr)
for v in arr:
    if counter[v] == 1:
        k -= 1
        if k == 0:
            return v
return ''