counter = Counter(nums)
hp = []
for num, freq in counter.items():
    if len(hp) == k:
        heappush(hp, (freq, num))
        heappop(hp)
    else:
        heappush(hp, (freq, num))
return [t[1] for t in hp]