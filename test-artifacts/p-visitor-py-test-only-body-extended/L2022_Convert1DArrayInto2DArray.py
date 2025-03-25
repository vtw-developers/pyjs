if m * n != len(original):
    return []
return [original[i:i + n] for i in range(0, m * n, n)]