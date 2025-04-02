cnt1 = Counter(words1)
cnt2 = Counter(words2)
return sum((cnt2[k] == 1 for k, v in cnt1.items() if v == 1))