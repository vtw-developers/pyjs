counter = Counter(students)
for i, sandwich in enumerate(sandwiches):
    if counter[sandwich] == 0:
        return len(students) - i
    counter[sandwich] -= 1
return 0