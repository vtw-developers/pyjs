counter = Counter(arr)
s = set()
for num in counter.values():
    if num in s:
        return False
    s.add(num)
return True