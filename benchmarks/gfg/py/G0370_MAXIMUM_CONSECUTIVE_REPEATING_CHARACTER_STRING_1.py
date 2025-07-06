def test():
  "--- test function ---"
  param =[('geeekk',),('3786868',),('110',),('aaaabbcbbb',),('11',),('011101',),('WoHNyJYLC',),('3141711779',),('10111101101',),('aabbabababcc',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    n = len(str_0)
    count = 0
    res = str_0[0]
    cur_count = 1
    for i in range(n):
        if i < n - 1 and str_0[i] == str_0[i + 1]:
            cur_count += 1
        else:
            if cur_count > count:
                count = cur_count
                res = str_0[i]
            cur_count = 1
    return res
"-----------------"
test()
