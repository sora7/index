from zipfile import ZipFile
import os

#dir with manga_ch1.zip .. manga_ch2.zip
processdir = r''

TEMPDIR = 'temp'
if not os.path.exists(TEMPDIR):
    os.mkdir(TEMPDIR)
FINALDIR = 'done'
if not os.path.exists(FINALDIR):
    os.mkdir(FINALDIR)

for fname in os.listdir(processdir):
    if fname.endswith('zip'):
        fname_full = os.path.join(processdir, fname)
        #print(fname)

        with ZipFile(fname_full, 'r') as z:
            z.extractall(TEMPDIR)

        for item in os.listdir(TEMPDIR):
            item_full = os.path.join(TEMPDIR, item)
            item_new = fname + '_-_' + item
            item_full_new = os.path.join(FINALDIR, item_new)
            os.rename(item_full, item_full_new)
