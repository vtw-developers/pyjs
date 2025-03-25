res = 0
for c in columnTitle:
    res = res * 26 + (ord(c) - ord('A') + 1)
return res