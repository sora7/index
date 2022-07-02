## BADCHAR
## RENAMES FORBIDDEN CHARACTERS

BADCHARS = ['/', '?', '<', '>', '\\', ':', '*', '|',]

##BADCHARS = ['1', '2', '3', ]
REPLACE_CHAR = ' '

import os

def check(name):
    for char in BADCHARS:
        if char in name:
            return True
    return False

def clean(name):
    for char in BADCHARS:
        if char in name:
            name = name.replace(char, REPLACE_CHAR)
    return name
        

def process(path):
    print('PROCESSING: ', path)

    for item in os.listdir(path):
        item_fullpath = os.path.join(path, item)
        
        if check(item):
##            print('CONTAINS BADCHARS: ', item)
            item_new = clean(item)
            print('CONTAINS BADCHARS: ', item, ' > ', item_new)
            item_new_fullpath = os.path.join(path, item_new)

            os.rename(item_fullpath, item_new_fullpath)
            item_fullpath = item_new_fullpath

        if os.path.isdir(item_fullpath):
            process(item_fullpath)


process('/media/xubuntu/temp_1/SAVED/')


















