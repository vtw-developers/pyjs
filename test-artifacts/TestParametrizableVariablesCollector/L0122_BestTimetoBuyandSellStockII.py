res = 0
for i in range(1, len(prices)):
    t = prices[i] - prices[i - 1]
    res += max(t, 0)
return res