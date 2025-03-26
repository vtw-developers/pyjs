ans = numBottles
while numBottles >= numExchange:
    numBottles -= numExchange - 1
    ans += 1
return ans