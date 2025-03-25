cnt = Counter(num)
return all((int(v) == cnt[str(i)] for i, v in enumerate(num)))