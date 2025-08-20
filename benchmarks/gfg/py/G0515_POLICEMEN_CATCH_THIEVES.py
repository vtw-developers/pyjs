def test():
  "--- test function ---"
  param = [('ABBDEEFGGGIJOPQQQQRRSUXYYcdhiiiikkllllmprrsttuxz', 48, 45), ('760101', 6, 3), ('P00T00000111111111', 18, 2), ('ykSisrizyfEUyGffsvvDvVSDKSfVgIJpjkRnmOLXyUykw', 45, 44), ('11588', 5, 2), ('T10011100010101000001000011100000P', 34, 14), ('AIKQQXZfg', 9, 8), ('7069751398001392552793393855046274046423', 40, 28), ('00011111111', 11, 10), ('DCPHGouPTGEUnEU', 15, 12)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(arr, n, k):
    i = 0
    l = 0
    r = 0
    res = 0
    thi = []
    pol = []
    while i < n:
        if arr[i] == "P":
            pol.append(i)
        elif arr[i] == "T":
            thi.append(i)
        i += 1
    while l < len(thi) and r < len(pol):
        if abs(thi[l] - pol[r]) <= k:
            res += 1
            l += 1
            r += 1
        elif thi[l] < pol[r]:
            l += 1
        else:
            r += 1
    return res
"-----------------"
test()
