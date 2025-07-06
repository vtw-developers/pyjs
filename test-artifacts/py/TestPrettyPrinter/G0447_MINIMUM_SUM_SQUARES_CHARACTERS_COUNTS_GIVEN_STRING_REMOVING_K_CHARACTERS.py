def f_gold(str, k):
    l = len(str)
    if k >= l:
        return 0
    frequency = [0] * MAX_CHAR
    for i in range(0, l):
        frequency[ord(str[i]) - 97] += 1
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