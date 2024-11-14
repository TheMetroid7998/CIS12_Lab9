import shelve, os, hashlib

"""Exercises 13.10.2"""
def replace_all(pattern, replace, file1, file2):
    with open (file1, 'r', encoding='utf-8') as source, open (file2, 'w', encoding='utf-8') as dest:
        for line in source:
            if pattern in line:
                line = line.replace(pattern, replace)
            dest.write(line)

"""Exercises 13.10.3"""
def add_word(string):
    word, key = q_prep(string)
    with shelve.open('anagram', 'n', writeback=True) as anagram_db:
        if key not in anagram_db:
            anagram_db[key] = [word]
        else:
            if string not in anagram_db[key]:
                anagram_list = anagram_db[key]
                anagram_list.append(word)
                anagram_db[key] = anagram_list

def q_prep(word):
    word = word.strip().lower()
    return word, ''.join(sorted(word))

"""Exercises 13.10.4"""
def walk(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path)

def md5_digest(filename):
    with open(filename, 'rb').read() as data:
        md5_hash = hashlib.md5()
        md5_hash.update(data)
        digest = md5_hash.hexdigest()
    return digest

def same_contents(path1, path2):
    with open(path1, 'rb').read() as data1, open(path2, 'rb').read() as data2:
        return data1 == data2

def is_image(path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp']
    if os.path.isfile(path):
        #print("Valid file path.")
        split_path = os.path.splitext(path)
        #print("Extension is", split_path[1])
        return split_path[1].lower() in [ext.lower() for ext in valid_extensions]
    else:
        return "Invalid Path"

#print(is_image(r'C:\Users\Conrad\Pictures\1162253.jpg', valid_extensions))

def add_path(path, shelf):
    if os.path.isfile(path):
        digest = md5_digest(path)
        with shelve.open(f'{shelf}', writeback=True) as img_shelf:
            if digest not in img_shelf:
                img_shelf[digest] = [path]
            else:
                if digest not in img_shelf[digest]:
                    img_list = img_shelf[digest]
                    img_list.append(digest)
                    img_shelf[digest] = img_list
    return

def walk_images(directory):
    for dir in os.listdir(directory):
        path = os.path.join(directory, dir)
        if os.path.isfile(path):
            is_image(path)
        elif os.path.isdir(path):
            walk_images(path)

def main():
    with open('CH13/photos/digests', 'n') as img_db:
        walk_images('CH13/photos')

    for digest, paths in img_db.items():
        if len(paths) > 1:
            print(paths)

if __name__ == '__main__':
    main()
