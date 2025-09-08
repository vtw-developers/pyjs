length = len(string_0)
if string_0[0] < "A" or string_0[0] > "Z":
    return False
if string_0[length - 1] != ".":
    return False
prev_state = 0
curr_state = 0
index = 1
while index < length:
    pirel_pre_ctx_spec_identifier