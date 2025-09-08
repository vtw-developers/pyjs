count_odd = 0
count_even = 0
for i in range(n):
    if a[i] & 1:
        count_odd += 1
    else:
        count_even += 1
if count_odd % 2 and count_even % 2:
    return False
else:
    pirel_pre_ctx_spec_identifier