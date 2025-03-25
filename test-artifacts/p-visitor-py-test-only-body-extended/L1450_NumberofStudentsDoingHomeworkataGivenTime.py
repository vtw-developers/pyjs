count, n = (0, len(startTime))
for i in range(n):
    count += startTime[i] <= queryTime <= endTime[i]
return count