INF = 1061109567
dist = [INF] * n
dist[src] = 0
for _ in range(k + 1):
    backup = dist.copy()
    for f, t, p in flights:
        dist[t] = min(dist[t], backup[f] + p)
return -1 if dist[dst] == INF else dist[dst]