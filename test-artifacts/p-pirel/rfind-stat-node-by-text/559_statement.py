if i <= t:
    maxRev[i] = max(maxRev[i - 1], revenue[nxtbb])
else:
    maxRev[i] = max(maxRev[i - t - 1] + revenue[nxtbb], maxRev[i - 1])