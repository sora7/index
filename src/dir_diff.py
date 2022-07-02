import os
import re
import datetime
import xml.etree.ElementTree as et
import xml.dom.minidom as md

PATH = 'e:/OneWayRoad/pic'
PATH = 'e:/VIDEO'

PATH = r'e:\OneWayRoad\pic\SH\1\da\e\_UNSORTED'
PATH1 = r'e:\OneWayRoad\pic'
XML_FILE = 'log.xml'


def dirstat(path):
    size = 0
    files = 0
    dirs = 0
    for item in os.listdir(path):
        item_fullpath = os.path.join(path, item)
        if os.path.isfile(item_fullpath):
            files += 1
            size += os.stat(item_fullpath).st_size
        elif os.path.isdir(item_fullpath):
            dirs += 1
            s, f, d = dirstat(item_fullpath)
            size += s
            files += f
            dirs += d
    return size, files, dirs


#pythonsucks
def removeAnnoyingLines(elem):
    hasWords = re.compile("\\w")
    for element in elem.iter():
        if not re.search(hasWords, str(element.tail)):
            element.tail=""
        if not re.search(hasWords, str(element.text)):
            element.text = ""


def prettyfy(el):
    xml_str = et.tostring(el.getroot(), encoding='utf-8', method='')
    return md.parseString(xml_str).toprettyxml()
    return md.parseString(xml_str).toprettyxml(indent='  ', newl='\n')


def ssep(n):
    return '{0:,}'.format(n).replace(',',' ')

def unsep(s):
    return int(s.replace(' ', ''))

def diff_shot(last_shot, shot):
    result = dict()
    result['files'] = str(int(shot['files']) - int(last_shot['files']))
    result['folders'] = str(int(shot['folders']) - int(last_shot['folders']))

    result['size'] = ssep(unsep(shot['size']) - unsep(last_shot['size']))

    #result['size'] = str(int(shot['size']) - int(last_shot['size']))
    return result


def write_xml(path, size, files, dirs):
    dt = datetime.datetime.now()
    ts = str(datetime.datetime.timestamp(dt))
    dt_s = dt.strftime('%Y-%m-%d %H:%M:%S')

    try:
        tree = et.parse(XML_FILE)
    except IOError:
        root = et.Element('DirDiff')
        tree = et.ElementTree(root)

    root = tree.getroot()
    cat_dict = dict([(catalog.attrib['path'], catalog) for catalog in root])

    try:
        cat = cat_dict[path]
    except KeyError:
        cat = et.SubElement(root, 'Directory')
        cat.attrib['path'] = path

    shot_list = sorted([shot for shot in cat], key=lambda x: x.attrib['datetime'])

    if len(shot_list) > 0:
        last_shot = shot_list[-1].attrib
    else:
        last_shot = dict()
        last_shot['files'] = '0'
        last_shot['folders'] = '0'
        last_shot['size'] = '0'

    shot = et.SubElement(cat, 'shot')
    shot.attrib['datetime'] = dt_s
    shot.attrib['files'] = str(files)
    shot.attrib['folders'] = str(dirs)
    shot.attrib['size'] = ssep(size)

    curr_diff = diff_shot(last_shot, shot.attrib)

    diff = et.SubElement(shot, 'diff')
    diff.attrib = curr_diff

    # tree.write(XML_FILE, encoding='utf-8', xml_declaration=True)
    #
    removeAnnoyingLines(tree)
    xml_pretty = prettyfy(tree)

    with open(XML_FILE, 'w') as fh:
        fh.write(xml_pretty)


def check_dir(path):
    size, files, dirs = dirstat(path)
##    stat = 'files:{:>5}|folders:{:>5}|total: {:>12}'.format(files, dirs, size)
##
##    print(stat)
    write_xml(path, size, files, dirs)

if __name__ == '__main__':
    check_dir(PATH)
    #check_dir(PATH1)




