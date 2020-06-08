
def chiper(s: str) -> str:
    result = ''
    for c in s:
        if c.islower():
            result += chr(219-ord(c))
        else:
            result += c
    return result

print(chiper('aBc'))
