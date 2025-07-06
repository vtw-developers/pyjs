def f_gold(str):
    stack = []
    for i in range(len(str)):
        stack.append(str[i])
    for i in range(len(str)):
        str[i] = stack.pop()