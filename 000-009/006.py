from typing import List

def char_n_gram(t: str, n:int=2) -> List[str]:
    results = []
    for i in range(0, len(t)-n+1):
        results.append(t[i:i+n])
    return results

T1 = 'paraparaparadise'
T2 = 'paragraph'

X = set(char_n_gram(T1))
Y = set(char_n_gram(T2))

print('X: ', X)
print('Y: ', Y)
print('X|Y: ', X|Y)
print('X&Y: ', X&Y)
print('X-Y: ', X-Y)

print('se' in X)
print('se' in Y)
