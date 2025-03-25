res = 0
while n != 0:
    n, t = divmod(n, k)
    res += t
return res