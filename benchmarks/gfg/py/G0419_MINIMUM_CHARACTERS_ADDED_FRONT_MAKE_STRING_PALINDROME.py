def test():
  "--- test function ---"
  param =[('aadaa',),('2674377254',),('11',),('0011000 ',),('26382426486138',),('111010111010',),('abccba',),('5191',),('1110101101',),('abcdecbe',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(s):
    l = len(s)
    i = 0
    j = l - 1
    while i <= j:
        if s[i] != s[j]:
            retval_0 = False
            return retval_0
        i += 1
        j -= 1
    retval_1 = True
    return retval_1
"-----------------"
test()
