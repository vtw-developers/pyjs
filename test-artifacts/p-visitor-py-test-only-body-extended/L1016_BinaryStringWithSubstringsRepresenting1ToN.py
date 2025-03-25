for i in range(n, n // 2, -1):
    if bin(i)[2:] not in s:
        return False
return True