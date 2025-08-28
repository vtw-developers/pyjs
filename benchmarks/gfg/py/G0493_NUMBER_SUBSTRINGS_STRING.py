def test():
  "--- test function ---"
  param =[('gZFGZsHCimLf',),('505357',),('011011101',),('ovfwP Osauz',),('92132238746026',),('01100',),('RaOWYQRfiWKSyC',),('861330202',),('001100010',),('uvpKlGUBLOMba',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    n = len(str_0)
    return int(n * (n + 1) / 2)
"-----------------"
test()
