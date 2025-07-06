def test():
  "--- test function ---"
  param =[("((a+b)+((c+d)))",),("(((a+(b)))+(c+d))",),("(((a+(b))+c+d))",),("((a+b)+(c+d))",),("(8582007)",),("((a+(b))+(c+d))",),("(PylsShEdKAE)",),('886980680541',),('001',),('jsVmFeOq',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(string_0):
    Stack = []
    for ch in string_0:
        if ch == ")":
            top = Stack.pop()
            elementsInside = 0
            while top != "(":
                elementsInside += 1
                top = Stack.pop()
            if elementsInside < 1:
                retval_0 = True
                return retval_0
        else:
            Stack.append(ch)
    retval_1 = False
    return retval_1
"-----------------"
test()
