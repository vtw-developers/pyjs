count = 0
m = {'type': 0, 'color': 1, 'name': 2}
return sum([item[m[ruleKey]] == ruleValue for item in items])