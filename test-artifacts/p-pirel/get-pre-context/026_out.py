length = len(N)
l = int((length) / 2)
count = 0
for i in range(l + 1):
    s = N[0:0 + i]
    l1 = len(s)
    t = N[i:l1 + i]
    pirel_pre_ctx_spec_identifier