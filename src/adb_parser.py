from zipfile import ZipFile
import xml.etree.ElementTree as et
import re
import os

ZIPFILE = r'./adb_import.zip'
XML_FILE = r'C:\Users\beater\Downloads\curl-7.65.1_3-win32-mingw\curl-7.65.1-win32-mingw\bin\imported from alist.txt_animedb.pl.html'


XPATH_PAGENAME = (
    './body/'
    'div[@id="layout-content"]/'
    'div[@id="layout-main"]/'
    'h1'
)


XPATH_PAGE_NAME_URL_ID = (
    './body/'
    'div[@id="layout-content"]/'
    'div[@id="layout-main"]/'
    'div[@class="g_content anime_all sidebar"]/'
    'div[@class="g_section info"]/'
    'div[@class="block"]/'
    'div[@class="data"]/'
    'div[@id="tabbed_pane"]/'
    'div[@class="g_bubble body"]/'
    'div[@id="tab_1_pane"]/'
    'div[@class="g_definitionlist"]/'
    'table/tbody/'
)


XPATH_TITLE = (
    './body/'
    'div[@id="layout-content"]/'
    'div[@id="layout-main"]/'
    'div[@class="g_content anime_all sidebar"]/'
    'div[@class="g_section info"]/'
    'div[@class="block"]/'
    'div[@class="data"]/'
    'div[@id="tabbed_pane"]/'
    'div[@class="g_bubble body"]/'
    'div[@id="tab_1_pane"]/'
    'div[@class="g_definitionlist"]/'
    'table/'
    'tbody/'
)

XPATH_TITLE_NAME = (
    XPATH_TITLE +
    'tr[@class="g_odd romaji"]/'
    'td[@class="value"]/'
    'span[@itemprop="name"]'
)

#print(XPATH_TITLE_NAME)

XPATH_TITLE_URL = (
    XPATH_TITLE +
    'tr[@class="g_odd romaji"]/'
    'td[@class="value"]/'
    'a[@class="shortlink"]'
             )

XPATH_TITLE_EPS = (
    XPATH_TITLE +
    'tr[@class="type"]/'
    'td[@class="value"]/'
    'span[@itemprop="numberOfEpisodes"]'
)

XPATH_TITLE_YEAR = (
    XPATH_TITLE +
    'tr[@class="g_odd year"]/'
    'td[@class="value"]/'
    'span[@itemprop="startDate"]'
)

XPATH_FILE_TYPE = (
    './body[@id="anidb"]'
)

XPATH_LIST_NAME = (
    './body/'
    'div[@id="layout-content"]/'
    'div[@id="layout-main"]/'
    'div[@class="g_content creator_all sidebar"]/'
    'div[@class="g_section creator_entry"]/'
    'div[@class="g_section info"]/'
    'div[@class="block"]/'
    'div[@class="data"]/'
    'div[@id="tabbed_pane"]/'
    'div[@class="g_bubble body"]/'
    'div[@id="tab_1_pane"]/'
    'div[@class="g_definitionlist"]/'
    'table/'
    'tbody/'
    'tr[@class="g_odd romaji mainname"]/'
    'td[@class="value"]/'
    'span[@itemprop="name"]'
)

XPATH_LIST_COMMON = (
    './body/'
    'div[@id="layout-content"]/'
    'div[@id="layout-main"]/'
    'div[@class="g_content creator_all sidebar"]/'
    'div[@class="g_section creator_entry"]/'
    'div[@class="tabbed_pane g_section tabbed_pane_main"]/'
    'div[@class="g_bubble body"]/'
)

XPATH_LIST_PERSON = (
    'div[@class="g_section character"]/'
    'div[@class="container"]/'
    'table/tbody/tr'
)

XPATH_LIST_COMPANY = (
    'div[@class="g_section staff"]/'
    'div[@class="container "]/'
    'table/tbody/tr'
)

XML_REPLACE = (
    ('<head>.*?/head>', ''),
    ('<br>', ''),
    ('<br />', ''),
    ('<hr>', ''),
    ('<hr />', ''),
    ('<form.*?/form>', ''),
    ('<meta.*?>', ''),

    # ('<picture>.*?</picture>', ''),
    ('<img .*?>', ''),
    ('</tr>\n\t</tr>', '</tr>'),
    ('</tr>', '</td></tr>'),
    ('</td>[\n\t]{0,}</td>', '</td>'),
    ('</th>[\n\t]{0,}</td>', '</th>'),

    ('&middot;', ''),
    ('&copy;', ''),
    ('itemscope itemtype="', 'itemtype="'),
    ('&', '&amp;'),
    # ('</tr>\n\t</tr>', '</tr>'),
    ('<aprimary', '<a primary=""'),
    ('<astandin title="', '<a class="standin"  title="'),
    ('[^a-z0-9 \-"/]>', ''),
    ('<[^a-z0-9 !\-"/]', ''),

    ('<br ', ''),
    ('<b.*? a=""></b>', ''),
    ('<blockquote>', ''),
    ('</blockquote>', ''),

    # ('<td rowspan=\"[0-9]\" class=\"thumb anime\"><a href=\"animedb.pl[?]'
    #  'show=anime&amp;amp;aid=[0-9]*?\" />\n\t*?</a></td>', ''),
    # ('/>[ \n].*?</a>', '/>'),
)


def mismatch(html_text):
    try:
        tree = et.ElementTree(et.fromstring(html_text))
    except et.ParseError as e:
        print(str(e))
        html_text = fix_mismatched_tag(html_text, e)
        with open('XML_OUT.html', 'w', encoding='utf-8', errors='replace') as fh:
            fh.write(html_text)
        tree = mismatch(html_text)
    else:
        return tree


def prepare_html(html_text):
    for src, dst in XML_REPLACE:
        html_text = re.sub(src, dst, html_text, flags=re.DOTALL)

    # with open('XML_OUT.html', 'w', encoding='utf-8', errors='replace') as fh:
    #     fh.write(html_text)

    tree = et.ElementTree(et.fromstring(html_text))
    # tree = mismatch(html_text)

    root = tree.getroot()
    return root


def safe_char(inp_str):
    UNSAFE = '<>"*:?|/\\'
    for c in UNSAFE:
        inp_str = inp_str.replace(c, '_')
    return inp_str


def safe_char2(inp_str):
    UNSAFE = '<>"*:?|/\\'

    out = []

    for c in inp_str:
        if c in UNSAFE:
            out.append('_')
        else:
            out.append(c)

    return ''.join(out)


def fix_mismatched_tag(html_text, excep):
    ex_str = str(excep)
    mismatch_regex = re.compile(r'mismatched tag: line ([0-9]{1,}?), column ([0-9]{1,}?)')
    badform_regex = re.compile(r'not well-formed [(]invalid token[)]: line ([0-9]{1,}?), column ([0-9]{1,}?)')

    html_lines = html_text.splitlines()
    with open('XML_OUT.html', 'w', encoding='utf-8', errors='replace') as fh:
        fh.write(html_text)

    if re.search(mismatch_regex, ex_str):
        line, col = re.findall(mismatch_regex, ex_str)[0]
        print(line, col)
        # line = int(line)
        # print(html_lines[line-1] )
        # html_lines[line-1] = ''
    elif re.search(badform_regex, ex_str):
        line, col = re.findall(badform_regex, ex_str)[0]
        print('badform ', line, col)

    return '\n'.join(html_lines)


def fix_mismatched_tag2(html_text, ex_string):
    print(ex_string)
    line = ex_string.split('mismatched tag: line ')[1]
    line = line.split(',')[0]
    line = int(line)
    html_lines = html_text.splitlines()
    chunk = '\n'.join(html_lines[0:line])
    # print(chunk)
    mismatched_tag = re.findall(re.compile('<([^/])[ ].*?>'), chunk)[::-1][0]
    # print(line, mismatched_tag)
    close_tag = '</' + mismatched_tag + '>'
    html_lines.insert(line-1, close_tag)
    # print('\n'.join(html_lines[line-10:line+2]))
    return '\n'.join(html_lines)


def check_type(html_text):
    root = prepare_html(html_text)

    item = root.find(XPATH_FILE_TYPE)
    file_type = item.attrib['class']

    return file_type


def clear_trash_chars(inp_str):
    TRASH = ('\n', '\t')
    for t in TRASH:
        if inp_str.count(t) > 0:
            inp_str = inp_str.replace(t, '')
    return inp_str


def parser_test(root):
    for item in root.findall('./body/'
                             'div[@id="layout-content"]/'
                             'div[@id="layout-main"]/'
                             'div[@class="g_content creator_all sidebar"]/'
                             'div[@class="g_section creator_entry"]/'
                             'div[@id="tabbed_pane_main_2"]/'
                             'div[@class="g_bubble body"]/'
                             'div[@class="pane anime_production_(major)"]/'
                             'div[@class="g_section staff"]/'
                             'div[@class="container "]/'
                             'table/tbody/tr'
                             ):
        if not 'data-parent' in item.attrib.keys():
            # for subitem in item.findall('./td[@class="eps"]/span'):
            #     print(subitem.tag, subitem.attrib, subitem.text)

            title_name = item.find('./td[@class="name anime"]/a').text
            title_url = item.find('./td[@class="name anime"]/a').attrib['href']
            title_id = ''

            title_type = item.find('./td[@class="type"]').text

            year = item.find('./td[@class="year"]').text
            title_year = clear_trash_chars(year)
            eps = item.find('./td[@class="eps"]').text
            if eps is None:
                eps = item.find('./td[@class="eps"]/span').text
            title_eps = clear_trash_chars(eps)

            # print(year, t, eps, title_name)
        # print(item.tag, item.attrib, item.text)
        # print()
        # char_name = item.find('./td[@class="name char"]/a').text
        # char_url = item.find('./td[@class="name char"]/a').attrib['href']


def parse_list_row(subitem):
    title = dict()

    title['name'] = subitem.find('./td[@class="name anime"]/a').text
    title['url'] = subitem.find('./td[@class="name anime"]/a').attrib['href']
    title['id'] = ''

    title['type'] = subitem.find('./td[@class="type"]').text

    year = subitem.find('./td[@class="year"]').text
    title['year'] = clear_trash_chars(year)
    eps = subitem.find('./td[@class="eps"]').text
    if eps is None:
        eps = subitem.find('./td[@class="eps"]/span').text
    title['eps'] = clear_trash_chars(eps)

    return title


def parse_list(html_text):
    title_list = dict()

    root = prepare_html(html_text)

    item = root.find(XPATH_LIST_NAME)
    title_list['name'] = item.text

    title_list['list'] = list()

    for item in root.findall(XPATH_LIST_COMMON):
        if item.attrib['class'] == 'pane voice_acting':
            # print('PERSON')
            for subitem in item.findall(XPATH_LIST_PERSON):
                title = parse_list_row(subitem)
                title_list['list'].append(title)
                print(title['type'], title['eps'], title['year'], title['name'])

        elif item.attrib['class'] == 'pane anime_production_(major)':
            # print('COMPANY')
            for subitem in item.findall(XPATH_LIST_COMPANY):
                if 'data-parent' not in subitem.attrib.keys():
                    title = parse_list_row(subitem)
                    title_list['list'].append(title)
                    print(title['type'], title['eps'], title['year'], title['name'])

    return title_list


def parse_title(html_text):
    root = prepare_html(html_text)

    title = dict()

    item = root.find(XPATH_TITLE_NAME)
    title['main_title'] = item.text

    item = root.find(XPATH_TITLE_URL)
    title['url'] = item.attrib['href']

    item = root.find(XPATH_TITLE_EPS)
    title['eps'] = item.text

    item = root.find(XPATH_TITLE_YEAR)
    title['year'] = item.text

    return title


def run():
    adb_dir = './adb_import/list'
    for item in os.listdir(adb_dir):
        item_fullpath = os.path.join(adb_dir, item)
        if os.path.isfile(item_fullpath):
            with open(item_fullpath, encoding='utf-8') as fh:
                html_text = fh.read()
                # print(item)
                # print(item, check_type(html_text))
                # title_name = parse_title(html_text)
                parse_list(html_text)


def run_rename():
    do_rename = False
    adb_dir = './adb_import'
    for item in os.listdir(adb_dir):
        item_fullpath = os.path.join(adb_dir, item)
        if os.path.isfile(item_fullpath):
            with open(item_fullpath, encoding='utf-8') as fh:
                html_text = fh.read()
                title_name = parse_title(html_text)

            if do_rename:
                new_name = safe_char(title_name) + '.html'

                new_fullpath = os.path.join(adb_dir, new_name)
                while os.path.exists(new_fullpath):
                    new_name = '_' + new_name
                    new_fullpath = os.path.join(adb_dir, new_name)

                print(item, ' -> ', new_name)
                os.rename(item_fullpath, new_fullpath)


def read_zip(zip_file_path):
    with ZipFile(zip_file_path, 'r') as zip_file:
        for item in zip_file.namelist()[:3]:
            if not item.endswith('/'): #isfile
                with zip_file.open(item) as html_file:
                    html_text = html_file.read()
                    parse_title(html_text)


#run()
#read_zip(ZIPFILE)
