def test():
  "--- test function ---"
  param =[(97,),(97,),(32,),(40,),(18,),(14,),(90,),(39,),(1,),(57,),(-1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(num):
    if num < 0:
        return False
    sum_0, n = 0, 1
    while sum_0 <= num:
        sum_0 = sum_0 + n
        if sum_0 == num:
            return True
        n += 1
    return False
"-----------------"
test()
