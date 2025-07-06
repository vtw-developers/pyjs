def f_gold(n):
    answer = [None] * (n + 1)
    answer[0] = 1
    i = 1
    while i <= n:
        answer[i] = answer[i - 1] * 3 + 2
        i = i + 1
    return answer[n]