import os

markPNG = 'PNG'
markJPG = 'JFIF'

extPNG = 'png'
extJPG = 'jpg'

folder = '.'

total = len(os.listdir(folder))
curr = 0
for item in os.listdir(folder):
    curr = curr + 1
    if item.endswith('jpg') or item.endswith('png'):
        name, ext = os.path.splitext(item)
        with open(item, 'rb') as fh:
            txt = str(fh.read(15))

        if markPNG in txt and extPNG not in ext:
            new_name = '.'.join([name, extPNG])
            os.rename(item, new_name)
                
        if markJPG in txt and extJPG not in ext:
            new_name = '.'.join([name, extJPG])
            os.rename(item, new_name)

    print('%s percent of %s total' % (curr/total*100, total))
