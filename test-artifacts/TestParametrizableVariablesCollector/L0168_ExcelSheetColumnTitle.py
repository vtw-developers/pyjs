res = []
while columnNumber:
    columnNumber -= 1
    res.append(chr(ord('A') + columnNumber % 26))
    columnNumber //= 26
return ''.join(res[::-1])