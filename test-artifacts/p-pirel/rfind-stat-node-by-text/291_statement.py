for i in range(0, M):
    for j in range(i, M):
        rem = (M - (i + j) % M) % M
        if rem < j:
            continue
        if i == j and rem == j:
            ans = ans + h[i] * (h[i] - 1) * (h[i] - 2) / 6
        elif i == j:
            ans = ans + (h[i] * (h[i] - 1) * h[rem] / 2)
        elif rem == j:
            ans = ans + h[j] * (h[j] - 1) * h[i] / 2
        else:
            ans = ans + h[i] * h[j] * h[rem]