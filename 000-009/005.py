from typing import List

TEXT = "I am an NLPer"

def char_n_gram(t: str, n:int=2) -> List[str]:
    results = []
    for i in range(0, len(t)-n+1):
        results.append(t[i:i+n])
    return results

def word_n_gram(t: str, n:int=2) -> List[List[str]]:
    words = t.split()
    results = []
    for i in range(0, len(words)-n+1):
        results.append(words[i:i+n])
    return results

print(char_n_gram(TEXT))
print(word_n_gram(TEXT))
