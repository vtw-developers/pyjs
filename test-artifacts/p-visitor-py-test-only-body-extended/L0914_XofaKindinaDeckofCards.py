vals = Counter(deck).values()
return reduce(gcd, vals) >= 2