def test():
  "--- test function ---"
  param =[('geeekk',),('3786868',),('110',),('aaaabbcbbb',),('11',),('011101',),('WoHNyJYLC',),('3141711779',),('10111101101',),('aabbabababcc',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    l = len(str_0)
    count = 0
    res = str_0[0]
    for i in range(l):
        cur_count = 1
        for j in range(i + 1, l):
            if str_0[i] != str_0[j]:
                break
            cur_count += 1
        if cur_count > count:
            count = cur_count
            res = str_0[i]
    return res
"-----------------"
test()
