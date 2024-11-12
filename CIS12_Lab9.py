
import json, os, random, re, sys

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

def process_books(*filepaths):
    for path in filepaths:
        read_book(path)

def load_file(filepath, *books, reverse=False):
    if os.path.exists(filepath):
        with open(filepath, 'r') as book:
            return json.load(book)
    else:
        process_books(*books)
        if reverse:
            save_file(filepath, pages)
            return pages
        codebook = generate_codebook()
        save_file(filepath, codebook)

def encrypt(codebook, message):
    ciphertext = []
    for char in message:
        index = random.randint(0, len(codebook[char]) - 1)
        ciphertext.append(codebook[char].pop(index))
    return '-'.join(ciphertext)


def decrypt(rev_book, ciphertext):
    plaintext = []
    for idx in re.findall(r'\d+-\d+-\d+-', ciphertext):
        page, line, char = idx.split('-')
        plaintext.append(rev_book[page][line][int(char)])
    return ''.join(plaintext)

def m_menu():
    print("""1. Encrypt\n2. Decrypt\n3. Quit""")
    return int(input("Make a selection [1, 2, 3]: \n"))


def main():
    books = ('books/dr_jekyll.txt', 'books/shakespeare.txt', 'books/war_and_peace.txt')
    codebook_path = 'codebooks/cd.json'
    rev_book_path = 'codebooks/rv.json'
    while True:
        try:
            mode = m_menu()
            match mode:
                case 1:
                    codebook = load_file(codebook_path, *books)
                    message = input("Enter plaintext: \n")
                    print(encrypt(codebook, message))
                    continue
                case 2:
                    reverse_book = load_file(rev_book_path, *books, reverse=True)
                    message = input("Enter ciphertext: \n")
                    print(decrypt(reverse_book, message))
                    continue
                case 3:
                    sys.exit(0)
        except ValueError as val_err:
            print("Invalid input.")

if __name__ == '__main__':
    main()