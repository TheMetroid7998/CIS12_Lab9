
def word_counter_generic(filename):
    """
    Creates a dictionary of `unique_words` and opens the given `filename` with alias `textfile`.
    For each line in the text file, take each word in the line,
    Replace any instances of dashes with spaces and split the word accordingly,
    Strip any instances of a given punctuation string and convert the word to lowercase,
    If the word is not empty, add it with a dictionary value of 1. If it is already present, raise the value by 1.
    Also, this version does not count unique punctuation relative to the file.
    """
    unique_words = {}
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            for word in line.replace('—', ' ').split():
                word = word.strip('.’;,-“”:?—‘!()_').lower()
                if word:
                    if word in unique_words:
                        unique_words[word] += 1
                    else:
                        unique_words[word] = 1
    return unique_words#,len(unique_words)

import unicodedata

def word_counter_specific(filename):
    """
    Creates a dictionary of `unique_words` and opens the given `filename` with alias `textfile`.
    Creates a string of unique punctuation symbols in the file with the function `punc_finder`.
    For each line in the text file, take each word in the line;
    Replace any instances of dashes with spaces and split the word accordingly,
    Strip any instances of the generated punctuation string and convert the word to lowercase,
    If the word is not empty, add it with a dictionary value of 1. If it is already present, raise the value by 1.
    """
    unique_words = {}
    punctuation = punc_finder(filename)
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            for word in line.replace('—', ' ').split():
                word = word.strip(punctuation).lower()
                if word:
                    if word in unique_words:
                        unique_words[word] += 1
                    else:
                        unique_words[word] = 1
    return unique_words#,len(unique_words)

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

def word_validator():
    valid_words = {}
    with open ('dictionary.txt', 'r', encoding='utf-8') as word_dict:
        for word in word_dict.read().split():
            valid_words[word.lower()] = 1
    return valid_words

def subtract(valid_dict, comp_dict):
    reserve = {}
    for key in comp_dict:
        if key not in valid_dict:
            reserve[key] = comp_dict[key]
    return reserve

#diff = subtract(word_validator(),word_counter_specific('dr_jekyll.txt'))
#common_counter(diff)

def singles_finder():
    single_instances = []
    diff = subtract(word_validator(), word_counter_specific('dr_jekyll.txt'))
    for word, freq in diff.items():
        if freq == 1:
            single_instances.append(word)
    return single_instances

import random

def random_wordgen(filename):
    words = list(word_counter_specific(filename))
    weights = list(word_counter_specific(filename).values())
    random_words = random.choices(words, weights=weights, k=6)
    print(' '.join(random_words))

#random_wordgen('dr_jekyll.txt')

bigram_dict = {}
window = []

def count_bigram(bigram):
    key = tuple(bigram)
    if key not in bigram_dict:
        bigram_dict[key] = 1
    else:
        bigram_dict[key] += 1

def process_word(word):
    window.append(word)
    if len(window) == 2:
        count_bigram(window)
        window.pop(0)

def bigram_counter():
    with open('dr_jekyll.txt', 'r', encoding='utf-8') as textfile:
        punctuation = punc_finder('dr_jekyll.txt')
        for line in textfile:
            for word in line.replace('—', ' ').split():
                word = word.strip(punctuation).lower()
                process_word(word)
    common_counter(bigram_dict)
#bigram_counter()

def random_bigram_gen():
    bigram_counter()
    bigrams = list(bigram_dict)
    weights = list(bigram_dict.values())
    random_bigrams = random.choices(bigrams, weights=weights, k=6)
    for pair in random_bigrams:
        print(' '.join(pair), end=' ')
#random_bigram_gen()

successor_map = {}
window2 = []
def add_bigram(bigram):
    first, second = bigram

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)

def process_bigram(word):
    window2.append(word)

    if len(window2) == 2:
        add_bigram(window2)
        window2.pop(0)

from pprint import pprint

def bigram_map(key):
    with open('dr_jekyll.txt', 'r', encoding = 'utf-8') as source:
        for line in source:
            for word in line.replace('—', ' ').split():
                word = word.strip('.’;,-“”:?—‘!()_').lower()
                process_bigram(word)
                #pprint(successor_map)
    print(successor_map[f'{key}'])
#bigram_map('going')

def random_sentence(word):
    bigram_map(word)
    for i in range(10):
        successors = successor_map[word]
        word = random.choice(successors)
        print(word, end=' ')

random_sentence('although')