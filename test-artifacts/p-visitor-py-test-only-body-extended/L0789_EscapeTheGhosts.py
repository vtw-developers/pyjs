'\n    :type ghosts: List[List[int]]\n    :type target: List[int]\n    :rtype: bool\n    '
flag = abs(target[0]) + abs(target[1])
for i in ghosts:
    if abs(i[0] - target[0]) + abs(i[1] - target[1]) <= flag:
        return False
else:
    return True