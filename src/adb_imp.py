from zipfile import ZipFile
import xml.etree.ElementTree as et
import re
import os
import sqlite3

FFDB_FILE = r'C:\Users\beater\AppData\Roaming\Moonchild Productions\Pale Moon\Profiles\newprofil\places.sqlite'

from loader import Loader
# import adb_parser
from adb_parser import *

ADB_PATH = './anidb-source'


def get_page_name_id_url(html_text):
    page_name, page_id, page_url = None, None, None

    root = prepare_html(html_text)

    for item in root.findall(
        './body/'
        'div[@id="layout-content"]/'
        'div[@id="layout-main"]/'
        'h1'
    ):
        page_class = item.get('class')
        if page_class == 'anime':
            for item in root.findall(
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
                'tr[@class="g_odd romaji"]/'
                'td[@class="value"]'
            ):
                for span in item.findall('span[@itemprop="name"]'):
                    page_name = span.text
                for a in item.findall('a[@class="shortlink"]'):
                    page_url = a.get('href')
                    page_id = a.text

        elif page_class == 'creator':
            for item in root.findall(
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
                'table/tbody/'
                'tr[@class="g_odd romaji mainname"]/'
                'td[@class="value"]'
            ):
                for span in item.findall('span[@itemprop="name"]'):
                    page_name = span.text
                for a in item.findall('a[@class="shortlink"]'):
                    page_url = a.get('href')
                    page_id = a.text
                # print(item, item.keys(), item.get('class'), item.text)

        elif page_class == 'tag':
            for item in root.findall(
                './body/'
                'div[@id="layout-content"]/'
                'div[@id="layout-main"]/'
                'div[@class="g_content tag_all sidebar"]/'
                'div[@class="g_section info"]/'
                'div[@class="block"]/'
                'div[@class="data"]/'
                'div[@id="tabbed_pane"]/'
                'div[@class="g_bubble body"]/'
                'div[@id="tab_1_pane"]/'
                'div[@class="g_definitionlist"]/'
                'table/tbody/'
                'tr[@class="g_odd main"]/'
                'td[@class="value"]'
            ):
                # print(item, item.keys(), item.get('class'), item.text)
                for span in item.findall('span[@itemprop="name"]'):
                    page_name = span.text
                for a in item.findall('a[@class="shortlink"]'):
                    page_url = a.get('href')
                    page_id = a.text

    return page_name, page_id, page_url, page_class


def get_page_name_id_url2(html_text):
    page_name, page_id, page_url = None, None, None

    root = prepare_html(html_text)

    for item in root.findall(
        './body/'
        'div[@id="layout-content"]/'
        'div[@id="layout-main"]/'
        'h1'
    ):
        page_class = item.get('class')
        if page_class == 'anime':
            for item in root.findall(
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
                'tr[@class="g_odd romaji"]/'
                'td[@class="value"]/'
                'span[@itemprop="name"]'
            ):
                page_name = item.text
            for item in root.findall(
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
                'tr[@class="g_odd romaji"]/'
                'td[@class="value"]/'
                'a[@class="shortlink"]'
            ):
                page_id = item.text
                page_url = item.get('href')
                # print(item, item.keys(), item.get('class'), item.text)

        elif page_class == 'creator':
            for item in root.findall(
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
                'table/tbody/'
                'tr[@class="g_odd romaji mainname"]/'
                'td[@class="value"]/'
                'span[@itemprop="name"]'
            ):
                page_name = item.text
            for item in root.findall(
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
                'table/tbody/'
                'tr[@class="g_odd romaji mainname"]/'
                'td[@class="value"]/'
                'a[@class="shortlink"]'
            ):
                page_id = item.text
                page_url = item.get('href')
                # print(item, item.keys(), item.get('class'), item.text)

    return page_name, page_id, page_url, page_class


def change_css_pic(html):
    XML_REPLACE = (
        ('src="https://cdn-eu.anidb.net/images/main/', 'src="./pic/'),
        ('href="https://cdn-eu.anidb.net/css/anidbstyle3/anidbstyle3.css.*?"',
         'href="./css/anidbstyle3.css"')
    )
    for src, dst in XML_REPLACE:
        html = re.sub(src, dst, html, flags=re.DOTALL)
    return html


def prepare_source():

    for filename in os.listdir(ADB_PATH):
        fullpath = os.path.join(ADB_PATH, filename)
        if os.path.isfile(fullpath):
            fname, ext = os.path.splitext(os.path.basename(filename))

            # print(fname)
            with open(fullpath, encoding='utf-8') as fh:
                html_text = fh.read()
                page_name, page_id, page_url, page_class = get_page_name_id_url(html_text)
                # print(page_name, page_id, page_url, page_class)

                new_fname = page_id + '_' + safe_char2(page_name) + '.htm'
                new_fullpath = os.path.join(ADB_PATH, new_fname)

            os.rename(fullpath, new_fullpath)


def check_old():
    old_ids = []
    old_id_regex = re.compile('[(]<a class="shortlink" href="http://anidb.net/([a-z0-9]{1,})">[a-z0-9]{1,}</a>[)]')
    for filename in os.listdir('./adb_import/old'):
        fullpath = os.path.join('./adb_import/old', filename)
        if os.path.isfile(fullpath):
            # print(filename)
            with open(fullpath, encoding='utf-8') as fh:
                text = fh.read()
                res = re.findall(old_id_regex, text)
                if len(res) > 0:
                    old_id = res[0]
                    old_ids.append(old_id[1:])
    return old_ids


def load():
    loader = Loader()
    html = loader.get_html('https://anidb.net/anime/782')
    with open('782.htm', 'w', encoding='utf-8') as fh:
        fh.write(html)


def make_txt(lst):
    prefix = 'https://anidb.net/anime/'
    # prefix = ''

    with open('list.txt', 'w') as fh:
        fh.write('\n'.join([prefix + item for item in lst]))


def pic_links():
    pic_urls = []
    pic_regex = re.compile('<meta property="og:image" content="(https://cdn-eu.anidb.net/images/main/[0-9]{1,}.jpg)"/>')
    for filename in os.listdir(ADB_PATH):
        fullpath = os.path.join(ADB_PATH, filename)
        if os.path.isfile(fullpath):
            with open(fullpath, encoding='utf-8') as fh:
                text = fh.read()
                res = re.findall(pic_regex, text)
                if len(res) > 0:
                    pic_url = res[0]
                    # print(pic_url)
                    pic_urls.append(pic_url)
    return pic_urls


def run():
    # prepare_source()
    # files = check_files()
    # ffdb = cheak_ffdb()
    #
    # ff_not_in_files = list(set(ffdb) - set(files))
    # print(ff_not_in_files)

    old = check_old()
    # old_not_in_ff = list(set(old) - set(ffdb))
    # print(old_not_in_ff)
    make_txt(old)
    # pic_urls = pic_links()
    # make_txt(pic_urls)


def cheak_ffdb():
    id_list = []
    with sqlite3.connect(FFDB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(
            "SELECT url FROM moz_places WHERE url LIKE '%anidb.net/anime%'"
        )
        for line in curs.fetchall():
            adb_id = line[0].split('/')[::-1][0]
            id_list.append(adb_id)
    return id_list


def check_files():
    id_list = []
    for filename in os.listdir(ADB_PATH):
        fullpath = os.path.join(ADB_PATH, filename)
        if os.path.isfile(fullpath):
            if filename.startswith('a'):
                adb_id = filename.split('_')[0][1:]
                'https://anidb.net/anime/13552'
                id_list.append(adb_id)
    return id_list


run()
