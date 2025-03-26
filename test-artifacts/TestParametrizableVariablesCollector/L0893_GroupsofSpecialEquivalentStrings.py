s = {''.join(sorted(word[::2]) + sorted(word[1::2])) for word in words}
return len(s)