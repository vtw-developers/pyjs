count = dict()
for i in range(n):
    if count.get(a[i]):
        count[a[i]] += 1
    else:
        count[a[i]] = 1
pirel_pre_ctx_spec_identifier