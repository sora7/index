import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os

path = 'Downloads.meta4'


def get_links(fname):
    links = list()
    doc = md.parse(fname)

    files = doc.getElementsByTagName('file')
##    print(files)

    for f in files:
        file_name = f.getAttribute('name')
        file_url = f.getAttribute('a0:referrer')
##        print(file_name, file_url)
        links.append((file_url, file_name))
        
##        file_name = file_name.split(' - ')[1]
##        file_name = file_name.split('.mp4')[0]
##        
##        link_name = file_name
##
##        file_name = file_name.lower()
##        file_name = file_name.replace(' ', '-')
##
##        file_number = f.getAttribute('name')
##        file_number = str(file_number).split('.mp4')[0]
##
##        url = list()
##        url.append('https://www.boundhub.com/videos')
##        url.append(file_number)
##        url.append(file_name)
##        url.append('')
##
##        link_url = '/'.join(url)

##        links.append((link_url, link_name))

    return links


def gen_html(links):
    html = list()
    html.append('<html><head><title>Links From BH</title></head><body>')
    html.append('<ol>')

    for url, title in links:
        html.append('<li><a href="%s">%s</a></li>\n' % (url, title))
    html.append('</ol>')
    html.append('</body></html>')

    with open('BH Links.html', 'w') as fh:
        fh.write(''.join(html))

def gen_html2(links):
    root = et.Element('html')
    head = et.SubElement(root, 'head')
    page_title = et.SubElement(head, 'title')
    page_title.text = 'Links From BH'
    body = et.SubElement(root, 'body')
    ol = et.SubElement(body, 'ol')
    
    for url, title in links:
        li = et.SubElement(ol, 'li')
        a = et.SubElement(li, 'a')
        a.attrib['href'] = url
        a.text = title

    tree = et.ElementTree(root)
    xml_str = et.tostring(tree.getroot(), encoding='utf-8', method='html')
    
    d1 = md.parseString(xml_str)
    xml_pretty = d1.toprettyxml()
    with open('BH Links.html', 'w', encoding='utf-8') as fh:
        fh.write(xml_pretty)

if __name__ == '__main__':
    links = get_links(path)
    gen_html2(links)
    os.system('pause')
