delta = [0] * 1000010
for start, end in intervals:
    delta[start] += 1
    delta[end] -= 1
return max(accumulate(delta))