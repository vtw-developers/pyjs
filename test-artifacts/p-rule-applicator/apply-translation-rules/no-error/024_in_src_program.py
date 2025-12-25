def test():
  "--- test function ---"
  param =["I love cinema.", "The vertex is S.", "I am single.", "My name is KG.", "I lovE cinema.", "GeeksQuiz. is a quiz site.", "I love Geeksquiz and Geeksforgeeks.", "  You are my friend.", "I love cinema", "Hello, world !", "Bond, James Bond.", "Trailing space ."]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(parameters_set)
"-----------------"
def f_gold(string_0):
    length = len(string_0)
    myexactlog(1, length)
    if string_0[0] < "A" or string_0[0] > "Z":
        myexactlog(2, 0)
        myexactlog(3, False)
        return False
    if string_0[length - 1] != ".":
        myexactlog(4, 1)
        myexactlog(5, False)
        return False
    prev_state = 0
    myexactlog(6, prev_state)
    curr_state = 0
    myexactlog(7, curr_state)
    index = 1
    myexactlog(8, index)
    while index < length:
        myexactlog(9, 0)
        myexactlog(10, string_0[index])
        break
"-----------------"
test()