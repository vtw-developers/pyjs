for i in range(n):
    curr_rem = sm[i] % k
    if not curr_rem and maxSum < sm[i]:
        maxSum = sm[i]
    elif not curr_rem in um:
        um[curr_rem] = i
    elif maxSum < (sm[i] - sm[um[curr_rem]]):
        maxSum = sm[i] - sm[um[curr_rem]]