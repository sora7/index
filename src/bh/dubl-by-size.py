import os
import re
import xml.dom.minidom as md
import xml.etree.ElementTree as et 
from pprint import pprint

files = []

def scan(path):
    if os.path.isfile(path):
        if path.endswith('.mp4'):
            files.append({'path':path, 'size':os.path.getsize(path)})
    elif os.path.isdir(path):
        for item in os.listdir(path):
            item_fullpath = os.path.join(path, item)
            scan(item_fullpath)


def dubl(files_list):
    temp = {}
    dubl_files = {}
    for f in files_list:
        fname, fsize = f['path'], f['size']
        if fsize not in temp.keys():
            temp[fsize] = fname
        else:
            if fsize not in dubl_files.keys():
                dubl_files[fsize] = []
                dubl_files[fsize].append(temp[fsize])
                dubl_files[fsize].append(fname)
            else:
                dubl_files[fsize].append(fname)

    return dubl_files

def space_split(n):
    return ' '.join(re.findall('.{1,3}', str(n)[::-1]))[::-1]

def gen_html2(files_list):
    root = et.Element('html')
    head = et.SubElement(root, 'head')
    
    page_title = et.SubElement(head, 'title')
    page_title.text = 'Duplicated Files (by Size)'

    meta = et.SubElement(head, 'meta')
    meta.attrib['charset'] = 'utf-8'
    
    body = et.SubElement(root, 'body')

    h2 = et.SubElement(body, 'h2')
    h2.text = 'Duplicated Files'

    dl = et.SubElement(body, 'dl')

    for size in sorted(files_list.keys(), reverse=True):
        dt = et.SubElement(dl, 'dt')
        dt.text = space_split(size)+' Bytes:'
        for item in files_list[size]:
            dd = et.SubElement(dl, 'dd')
            f_path, f_name = os.path.split(item)
            dd.text = os.path.join(f_path, 'zzz_'+f_name)
        br = et.SubElement(dl, 'br')
        
    tree = et.ElementTree(root)
    xml_str = et.tostring(tree.getroot(), encoding='utf-8', method='html')
    
#    d1 = md.parseString(xml_str)
#    xml_pretty = d1.toprettyxml()
    xml_pretty = xml_str.decode('utf-8')
##    print(xml_pretty)
    with open('DB Files.html', 'w', encoding='utf-8') as fh:
        fh.write(xml_pretty)

def ren_dub(files_list):
    for size in sorted(files_list.keys(), reverse=True):
        for item in files_list[size]:
            file_path, file_name = os.path.split(item)
            new_file_path = os.path.join(file_path, 'zzz_' + file_name)
            os.rename(item, new_file_path)
            

scan(r'l:\_\_bh')

dub = dubl(files)

ren_dub(dub)

gen_html2(dub)



