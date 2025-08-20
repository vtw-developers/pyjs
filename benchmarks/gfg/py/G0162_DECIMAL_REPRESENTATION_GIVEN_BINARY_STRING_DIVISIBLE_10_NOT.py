def test():
  "--- test function ---"
  param =[('101000',),('39613456759141',),('11',),('PoiHjo',),('2',),('0000101',),('T  s dZKeDX gK',),('3944713969',),('1000',),('ifYUgdpmt',),('100',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(bin_0):
    n = len(bin_0)
    if bin_0[n - 1] == "1":
        return False
    sum_0 = 0
    i = n - 2
    while i >= 0:
        if bin_0[i] == "1":
            posFromRight = n - i - 1
            if posFromRight % 4 == 1:
                sum_0 = sum_0 + 2
            elif posFromRight % 4 == 2:
                sum_0 = sum_0 + 4
            elif posFromRight % 4 == 3:
                sum_0 = sum_0 + 8
            else:
                sum_0 = sum_0 + 6
        i = i - 1
    if sum_0 % 10 == 0:
        return True
    return False
"-----------------"
test()
