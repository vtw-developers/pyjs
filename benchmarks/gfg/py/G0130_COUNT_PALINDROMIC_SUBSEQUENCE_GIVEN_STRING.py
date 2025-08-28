def test():
  "--- test function ---"
  param =[('R',),('2956350',),('11100111110101',),('TZTDLIIfAD',),('98',),('1100100001',),('oKwGeatf',),('19',),('00010110100',),('Cyq',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    N = len(str_0)
    cps = [[0 for i in range(N + 2)] for j in range(N + 2)]
    for i in range(N):
        cps[i][i] = 1
    for L in range(2, N + 1):
        for i in range(N):
            k = L + i - 1
            if k < N:
                if str_0[i] == str_0[k]:
                    cps[i][k] = cps[i][k - 1] + cps[i + 1][k] + 1
                else:
                    cps[i][k] = cps[i][k - 1] + cps[i + 1][k] - cps[i + 1][k - 1]
    return cps[0][N - 1]
"-----------------"
test()
