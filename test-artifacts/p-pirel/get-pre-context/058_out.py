l = 0
h = len(string_0) - 1
while h > l:
    l += 1
    h -= 1
    if string_0[l - 1] != string_0[h + 1]:
        return False
pirel_pre_ctx_spec_identifier