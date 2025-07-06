def f_gold(A, B, n):
    mp = set()
    result = 0
    curr_sum = curr_begin = 0
    for i in range(0, n):
        while A[i] in mp:
            mp.remove(A[curr_begin])
            curr_sum -= B[curr_begin]
            curr_begin += 1
        mp.add(A[i])
        curr_sum += B[i]
        result = max(result, curr_sum)
    return result