
"""12.12.1"""
successor_map = {}
def add_bigram(bigram):
    first, second = bigram
    successor_map.setdefault(first, []).append(second)

"""12.12.2"""
import unicodedata

def punc_finder(filename):
    """
    Creates a dictionary of punctuation marks that will be generated.
    Opens the given `filename` with alias `textfile`,
    For each line and each character in that line,
    If the character's Unicode category can be identified as punctuation,
    Add the character to the `punc_marks` dictionary with a placeholder value of 1.
    Finally, join the dictionary and return the string `punctuation`.
    """
    punc_marks = {}
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            for char in line:
                category = unicodedata.category(char)
                if category.startswith('P'):
                    punc_marks[char] = 1
        punctuation = ''.join(punc_marks)
    return punctuation
def common_counter(dict_items, num=5):
    items = sorted(dict_items.items(), key=lambda x : x[1] , reverse=True)
    for word, freq in items[:num]:
        print(freq, word, sep='\t')

trigram_dict = {}
trigram_window = []

def count_trigram(trigram):
    key = tuple(trigram)
    if key not in trigram_dict:
        trigram_dict[key] = 1
    else:
        trigram_dict[key] += 1

def process_word(word):
    trigram_window.append(word)
    if len(trigram_window) == 3:
        count_trigram(trigram_window)
        trigram_window.pop(0)

def trigram_counter():
    with open('dr_jekyll.txt', 'r', encoding='utf-8') as textfile:
        punctuation = punc_finder('dr_jekyll.txt')
        for line in textfile:
            for word in line.replace('—', ' ').split():
                word = word.strip(punctuation).lower()
                process_word(word)
    common_counter(trigram_dict)

#trigram_counter() #kinda broken but whatever

"""12.12.3"""
def add_trigram(trigram):
    first, second, third = trigram
    key = (first, second)
    successor_map.setdefault(key, []).append(third)

def process_word_trigram(word):
    trigram_window.append(word)
    if len(trigram_window) == 3:
        add_trigram(trigram_window)
        trigram_window.pop(0)

"""12.12.4"""
import random
window2 = []
def process_bigram(word):
    window2.append(word)

    if len(window2) == 2:
        add_bigram(window2)
        window2.pop(0)

def bigram_map(key):
    with open('dr_jekyll.txt', 'r', encoding = 'utf-8') as source:
        for line in source:
            for word in line.replace('—', ' ').split():
                word = word.strip('.’;,-“”:?—‘!()_').lower()
                process_bigram(word)
    #print(successor_map[f'{key}'])
    successor_map2 = {key:successor_map[f'{key}']}
    print(successor_map2)
bigram_map('although')
successors = list(successor_map)
bigram = random.choices(successors, k=2)
print(bigram)