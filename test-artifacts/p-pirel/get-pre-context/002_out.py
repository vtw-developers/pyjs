m = 1
while x & m:
    x = x ^ m
    m <<= 1
x = x ^ m
pirel_pre_ctx_spec_identifier