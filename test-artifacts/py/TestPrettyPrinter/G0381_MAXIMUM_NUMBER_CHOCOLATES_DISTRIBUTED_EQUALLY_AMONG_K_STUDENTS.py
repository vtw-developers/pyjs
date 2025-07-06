def f_gold(arr, n, k):
    um, curr_rem, maxSum = {}, 0, 0
    sm = [0] * n
    sm[0] = arr[0]
    for i in range(1, n):
        sm[i] = sm[i - 1] + arr[i]
    for i in range(n):
        curr_rem = sm[i] % k
        if not curr_rem and maxSum < sm[i]:
            maxSum = sm[i]
        elif not curr_rem in um:
            um[curr_rem] = i
        elif maxSum < (sm[i] - sm[um[curr_rem]]):
            maxSum = sm[i] - sm[um[curr_rem]]
    return maxSum // k