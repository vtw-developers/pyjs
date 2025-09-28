def test():
  "--- test function ---"
  param =[(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    dp = [[0 for j in range(27)] for i in range(n + 1)]
    for i in range(0, 26):
        dp[1][i] = 1
    for i in range(2, n + 1):
        for j in range(0, 26):
            if j == 0:
                dp[i][j] = dp[i - 1][j + 1]
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j + 1]
    sum_0 = 0
    for i in range(0, 26):
        sum_0 = sum_0 + dp[n][i]
    return sum_0
"-----------------"
test()
