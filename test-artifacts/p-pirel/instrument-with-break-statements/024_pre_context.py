n = len(s1)
m = len(s2)
dp = [[False for i in range(m + 1)] for i in range(n + 1)]
dp[0][0] = True
for i in range(len(s1)):
    for j in range(len(s2) + 1):
        pirel_pre_ctx_spec_identifier