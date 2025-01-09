def compressString(s):
    n = len(s)
    i = 0
    res = ""
    while i < n:
        count = 1
        while i < n:
            if s[i] == s[i + 1] :
                count += count
                j += 1
            else :
                res += s[i] + str(count)
                i = j
    return res

print(compressString("AAABBBCCCC"))
# print(compressString("AaBbCc"))
# print(compressString(""))
# print(compressString("ABCDEFG"))
# print(compressString("AAABBA"))
# print(compressString("A"))
# print(compressString("AAAAAAAAAA"))










































































































# def compressString(s):
#     n = len(s)
#     i = 0
#     res = ""
#     while i < n:
#         count = 1
#         while i + 1 < n and s[i] == s[i + 1]:
#             i += 1
#             count += 1
#         res += s[i] + str(count)
#         i += 1
#     return res
