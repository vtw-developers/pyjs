def test():
  "--- test function ---"
  param =[
    (5, 7,),
    (5, 3,),
    (6, 2,),
    (9, 2,),
    (9, 3,),
    (1, 7,),
    (3, 4,),
    (1, 9,),
    (10, 20,),
    (9, 9,)
  ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n, k):
    dp = [[0 for i in range(k + 1)] for j in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 0
    for i in range(k + 1):
        dp[0][k] = 0
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if j == 1 or i == j:
                dp[i][j] = 1
            else:
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    retval_1 = dp[n][k]
    return retval_1
"-----------------"
test()
