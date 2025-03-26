count_chars = Counter(s)
required = len(s) // 4
more_chars = defaultdict(int)
for char, count_char in count_chars.items():
    more_chars[char] = max(0, count_char - required)
min_len = len(s)
need_replace = sum(more_chars.values())
if need_replace == 0:
    return 0
first_cursor, second_cursor = (0, 0)
while second_cursor < len(s):
    if more_chars[s[second_cursor]] > 0:
        need_replace -= 1
    more_chars[s[second_cursor]] -= 1
    second_cursor += 1
    while first_cursor < second_cursor and need_replace == 0:
        min_len = min(min_len, second_cursor - first_cursor)
        if s[first_cursor] in more_chars:
            more_chars[s[first_cursor]] += 1
            if more_chars[s[first_cursor]] > 0:
                need_replace += 1
        first_cursor += 1
return min_len