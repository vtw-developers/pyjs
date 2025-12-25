def test():
  "--- test function ---"
  param = [
    ([[[0]]], [], 0, [], 0, 0),
    ([[[-1]]], [0], 0, [1], 0, 0),
    ([[[-1]]], [1], 0, [1], 0, 0),
        ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(dp, arr1, n, arr2, m, k):
    if k < 0:
        myexactlog(1, 0)
        myexactlog(2, -(10 ** 7))
        return -(10 ** 7)
    if n < 0 or m < 0:
        myexactlog(3, 1)
        myexactlog(4, 0)
        return 0
    ans = dp[n][m][k]
    myexactlog(5, ans)
    if ans != -1:
        myexactlog(6, 2)
        myexactlog(7, ans)
        return ans
    ans = max(f_gold(dp, arr1, n - 1, arr2, m, k), f_gold(dp, arr1, n, arr2, m - 1, k))
    myexactlog(8, ans)
    if arr1[n - 1] == arr2[m - 1]:
        myexactlog(9, 3)
        pass
"-----------------"
test()