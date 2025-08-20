def test():
  "--- test function ---"
  param = [('aaccddeeffhlloptuvwzabffhhijqyyz', 32, 21), ('xhhzxsfh', 8, 7), ('abbceeeflmmmmooppqstwyzaabdefikllnnnppqrrtuuuuuxx', 49, 4), ('nttoipfrxipecmrcueoejcdgl', 25, 2)]
  for i, parameters_set in enumerate(param):
    idx = i
    f_gold(* parameters_set)
    result = parameters_set
"-----------------"
def f_gold(s, n, k):
    t = ""
    last = 0
    cnt = 0
    new_last = 0
    size = 0
    string_0 = "zyxwvutsrqponmlkjihgfedcba"
    for ch in string_0:
        cnt = 0
        for i in range(last, n):
            if s[i] == ch:
                cnt += 1
        if cnt >= k:
            for i in range(last, n):
                if s[i] == ch:
                    t += ch
                    new_last = i
                    size += 1
            last = new_last
    return t
"-----------------"
test()
