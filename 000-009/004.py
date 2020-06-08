text = """
Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.
"""
words = text.replace('.', '').split()

targets = [1, 5, 6, 7, 8, 9, 15, 16, 19]
results = dict()
for i, word in enumerate(words, start=1):
    if i in targets:
        c_size = 1
    else:
        c_size = 2
    
    results[word[:c_size]] = i

print(results)
