import os
import datetime

import index

##path = 'e:/GAMES/Kino/Konosuba/'


def from_ts(timestamp, fmt='dt'):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M:%S')


def dir_stat(path):
    stat_info = os.stat(path)
    return {
        'dir': os.path.basename(path),
        'created': stat_info.st_ctime,
        'modified': stat_info.st_mtime
        }


def dir_info(path):
    info_list = []

    for item in os.listdir(path):
        item_fullpath = os.path.join(path, item)
        if os.path.isdir(item_fullpath):
            info_list.append(dir_stat(item_fullpath))
    return info_list


def print_info(lst):
    print('Created\t\t\tPath')
    for item in lst:
        print('%s | %s'%(
            from_ts(item['created']),
            item['dir'])
              ) 
        
##info = dir_info(path)
##print_info(info)
##print_info(sorted(info, key=lambda item: item['created'], reverse=True))



def process_dir_fast(dir_path):
    print(dir_path)
    info = dir_info(dir_path)
    print_info(sorted(info, key=lambda item: item['created'], reverse=True))


def process_dir(dir_path):
    stat_list = []
    for location in os.listdir(dir_path):
        location_full = os.path.join(dir_path, location)
        if os.path.isdir(location_full):
            # step into
            for item in os.listdir(location_full):
                item_full = os.path.join(location_full, item)
                if os.path.isdir(item_full) and index.TITLENAME_REGEX.match(item):
                    stat_list.append(dir_stat(item_full))
    return stat_list
                    
        
        
titles_dirs = (
    'i:/',
    'j:/',
    'k:/',
    'l:/',
    )
lst = []
for title_dir in titles_dirs:
    lst.extend(process_dir(title_dir))

print_info(sorted(lst, key=lambda item: item['created'], reverse=True))












