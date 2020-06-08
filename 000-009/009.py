import random

TEXT = 'I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind'

words = TEXT.split()
results = []
for w in words:
    if len(w) <= 4:
        results.append(w)
        continue
    w_s = w[0] + "".join(random.sample(list(w[1:-1]), len(w)-2)) + w[-1]
    results.append(w_s)

print(' '.join(results))
    