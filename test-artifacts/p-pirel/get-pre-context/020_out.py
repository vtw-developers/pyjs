l = len(num1)
num = list(num1)
i = l - 1
while i >= 0:
    if num[i] == "0":
        num[i] = "1"
        break
    else:
        num[i] = "0"
    i -= 1
num1 = "".join(num)
if i < 0:
    num1 = "1" + num1
pirel_pre_ctx_spec_identifier