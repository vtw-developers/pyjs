rows = {min(row) for row in matrix}
cols = {max(col) for col in zip(*matrix)}
return list(rows & cols)