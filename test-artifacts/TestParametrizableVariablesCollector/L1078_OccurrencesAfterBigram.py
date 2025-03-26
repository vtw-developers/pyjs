words = text.split(' ')
return [words[i + 2] for i in range(len(words) - 2) if words[i] == first and words[i + 1] == second]