def f_gold(m, x, revenue, n, t):
    maxRev = [0] * (m + 1)
    nxtbb = 0
    for i in range(1, m + 1):
        if nxtbb < n:
            if x[nxtbb] != i:
                maxRev[i] = maxRev[i - 1]
            else:
                if i <= t:
                    maxRev[i] = max(maxRev[i - 1], revenue[nxtbb])
                else:
                    maxRev[i] = max(maxRev[i - t - 1] + revenue[nxtbb], maxRev[i - 1])
                nxtbb += 1
        else:
            maxRev[i] = maxRev[i - 1]
    return maxRev[m]