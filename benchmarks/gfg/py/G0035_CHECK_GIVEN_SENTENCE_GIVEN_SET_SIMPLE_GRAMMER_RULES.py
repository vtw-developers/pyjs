def test():
  "--- test function ---"
  param =["I love cinema.", "The vertex is S.", "I am single.", "My name is KG.", "I lovE cinema.", "GeeksQuiz. is a quiz site.", "I love Geeksquiz and Geeksforgeeks.", "  You are my friend.", "I love cinema", "Hello world !"]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(parameters_set)
"-----------------"
def f_gold(string):
    length = len(string)
    if string[0] < "A" or string[0] > "Z":
        retval_0 = False
        return retval_0
    if string[length - 1] != ".":
        retval_1 = False
        return retval_1
    prev_state = 0
    curr_state = 0
    index = 1
    while string[index]:
        if string[index] >= "A" and string[index] <= "Z":
            curr_state = 0
        elif string[index] == " ":
            curr_state = 1
        elif string[index] >= "a" and string[index] <= "z":
            curr_state = 2
        elif string[index] == ".":
            curr_state = 3
        if prev_state == curr_state and curr_state != 2:
            retval_2 = False
            return retval_2
        if prev_state == 2 and curr_state == 0:
            retval_3 = False
            return retval_3
        if curr_state == 3 and prev_state != 1:
            retval_4 = True
            return retval_4
        index += 1
        prev_state = curr_state
    retval_5 = False
    return retval_5
"-----------------"
test()
