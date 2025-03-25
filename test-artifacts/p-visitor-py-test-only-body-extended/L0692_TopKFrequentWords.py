counter = Counter(words)
res = sorted(counter, key=lambda word: (-counter[word], word))
return res[:k]