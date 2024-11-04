
import json

LIBRARY = 3
LINE = 128
PAGE = 64
char_window = []
line_number = 0
line_window = {}
page_number = 0
pages = {}

def clean_line(line):
    return line.strip().replace('—', ' ') + ' '

def add_line():
    global char_window, line_number
    line_number += 1
    process_page(''.join(char_window), line_number)
    char_window.clear()

def add_page():
    global line_window, line_number, page_number, pages
    page_number += 1
    pages[page_number] = dict(line_window)
    line_window.clear()
    line_number = 0

def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def process_page(line, line_num):
    global line_number, line_window, pages, page_number
    line_window[line_num] = line
    if len(line_window) == PAGE:
        add_page()

def read_book(filename):
    global char_window
    with open(filename, 'r', encoding='utf-8-sig') as textfile:
        for line in textfile:
            line = clean_line(line)
            if line.strip():
                for char in line:
                    process_char(char)
    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()
    return

def generate_codebook():
    global pages
    codebook = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                codebook.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return codebook

def save_file(filepath, element):
    with open(filepath, 'w') as output:
        json.dump(element, output, indent=4)

def main():
    book = 'books/dr_jekyll.txt'
    read_book(book)
    codebook = generate_codebook()
    save_file('codebooks/codebook.json', codebook)
    save_file('codebooks/pages.json', pages)

if __name__ == '__main__':
    main()