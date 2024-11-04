
import unicodedata

def clean_line(line):
    return line.strip().replace('—', ' ') + ' '

def read_book(filename):
    punctuation = punc_finder(filename)
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            for word in clean_line(line).split():
                word = word.strip(punctuation).lower()
    return

def punc_finder(filename):
    punc_marks = {}
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            for char in line:
                category = unicodedata.category(char)
                if category.startswith('P'):
                    punc_marks[char] = 1
        punctuation = ''.join(punc_marks)
    return punctuation