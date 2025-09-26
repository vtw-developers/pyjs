if arr[i] == arr[i + 1]:
    count += 1
    continue
else:
    max_count = max(max_count, count)
    min_count = min(min_count, count)
    count = 0