frequency = dict()
for i in range(start, end + 1):
    if arr[i] in frequency.keys():
        frequency[arr[i]] += 1
    else:
        frequency[arr[i]] = 1
count = 0
for x in frequency:
    if x == frequency[x]:
        pirel_pre_ctx_spec_identifier