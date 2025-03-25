INF = 16191
g = defaultdict(list)
for u, v, w in times:
    g[u - 1].append((v - 1, w))
dist = [INF] * n
dist[k - 1] = 0
q = [(0, k - 1)]
while q:
    _, u = heappop(q)
    for v, w in g[u]:
        if dist[v] > dist[u] + w:
            dist[v] = dist[u] + w
            heappush(q, (dist[v], v))
ans = max(dist)
return -1 if ans == INF else ans