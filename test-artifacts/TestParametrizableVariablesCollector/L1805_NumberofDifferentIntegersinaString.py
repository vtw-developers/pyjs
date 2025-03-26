nums = re.split('[a-z]+', word)
return len({int(num) for num in nums if num != ''})