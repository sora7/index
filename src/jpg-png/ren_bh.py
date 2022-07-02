import os
import re

extPNG = 'png'
extJPG = 'jpg'

folder = '.'

regex = re.compile('[0-9]{3}_[0-9]{3}_([0-9]*).* - (.*?)[.]([A-Za-z]{3})')

total = len(os.listdir(folder))
curr = 0
for item in os.listdir(folder):
    curr = curr + 1
    if os.path.isfile(item):
        if item.endswith(extJPG) or item.endswith(extPNG):
            num, name, ext = re.findall(regex, item)[0]
            new_name = '_'.join([name, num])
            new_name = '.'.join([new_name, ext])
            os.rename(item, new_name)

    print('%s percent of %s total' % (curr/total*100, total))
