def test():
  "--- test function ---"
  param =[('SgUmIrEAB',),('304',),('0010',),('VGC BeErLvQ',),('0872',),('00110001',),('Lsqwm',),('308998',),('1000011',),('XCEOs',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    NO_OF_CHARS = 256
    count = [0] * NO_OF_CHARS
    for i in range(len(str_0)):
        count[ord(str_0[i])] += 1
    first, second = 0, 0
    for i in range(NO_OF_CHARS):
        if count[i] > count[first]:
            second = first
            first = i
        elif count[i] > count[second] and count[i] != count[first]:
            second = i
    retval_1 = chr(second)
    return retval_1
"-----------------"
test()
