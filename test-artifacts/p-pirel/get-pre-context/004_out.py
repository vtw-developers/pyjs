while y != 0:
    carry = x & y
    x = x ^ y
    y = carry << 1
pirel_pre_ctx_spec_identifier