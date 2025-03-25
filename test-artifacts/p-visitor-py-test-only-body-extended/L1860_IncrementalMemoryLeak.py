i = 1
while memory1 >= i or memory2 >= i:
    if memory1 >= memory2:
        memory1 -= i
    else:
        memory2 -= i
    i += 1
return [i, memory1, memory2]