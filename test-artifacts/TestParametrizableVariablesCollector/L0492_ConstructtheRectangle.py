w = int(sqrt(area))
while area % w != 0:
    w -= 1
return [area // w, w]