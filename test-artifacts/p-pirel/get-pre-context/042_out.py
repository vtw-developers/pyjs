diag1_left = 0
diag1_right = 0
diag2_left = 0
diag2_right = 0
i = 0
j = n - 1
while i < n:
    if i < n // 2:
        diag1_left += mat[i][i]
        diag2_left += mat[j][i]
    elif i > n // 2:
        diag1_right += mat[i][i]
        diag2_right += mat[j][i]
    i += 1
    j -= 1
pirel_pre_ctx_spec_identifier