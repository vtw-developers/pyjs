counter = Counter(arr)
t = sorted(counter.items(), key=lambda x: x[1])
for v, cnt in t:
    if k >= cnt:
        k -= cnt
        counter.pop(v)
    else:
        break
return len(counter)