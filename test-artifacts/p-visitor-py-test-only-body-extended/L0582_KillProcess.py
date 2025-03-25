def dfs(u):
    ans.append(u)
    for v in g[u]:
        dfs(v)
g = defaultdict(list)
n = len(pid)
for c, p in zip(pid, ppid):
    g[p].append(c)
ans = []
dfs(kill)
return ans