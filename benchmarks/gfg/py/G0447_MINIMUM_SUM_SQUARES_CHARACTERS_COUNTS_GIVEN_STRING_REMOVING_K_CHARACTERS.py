def test():
  "--- test function ---"
  param =[('JlIgDXBFbCeFRB', 8,),('41122661', 1,),('011', 1,),('hOCcIOAJztdT', 8,),('155799263', 7,),('1111', 3,),('Egy', 0,),('6900599415', 6,),('101010011111', 9,),('IbmRqJcU', 21,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
from queue import PriorityQueue
def f_gold(str_0, k):
    MAX_CHAR = 127
    l = len(str_0)
    if k >= l:
        return 0
    frequency = [0] * MAX_CHAR
    for i in range(0, l):
        frequency[ord(str_0[i]) - 97] += 1
    q = PriorityQueue()
    for i in range(0, MAX_CHAR):
        q.put(-frequency[i])
    while k > 0:
        temp = q.get()
        temp = temp + 1
        q.put(temp, temp)
        k = k - 1
    result = 0
    while not q.empty():
        temp = q.get()
        temp = temp * (-1)
        result += temp * temp
    return result
"-----------------"
test()
