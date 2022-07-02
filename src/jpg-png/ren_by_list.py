import os

path = '.'

with open(path+r'\list.txt') as fh:
	names = fh.read().split('\n')

for item in os.listdir(path):
    if not item.endswith('txt'):
        os.rename(path+'/'+item, path+'/'+names[n])
	n += 1
