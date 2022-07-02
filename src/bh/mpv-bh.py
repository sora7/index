import subprocess
import xml.dom.minidom
from pprint import pprint

cli_command = '''wmic process where "name='mpv.exe'" get commandline /format:rawxml'''

filelist = subprocess.Popen(cli_command, shell=True, stdout=subprocess.PIPE)
filelist, err = filelist.communicate()
filelist = filelist.decode('cp866', 'ignore')

print(filelist)

doc = xml.dom.minidom.parseString(filelist)
results = doc.getElementsByTagName('RESULTS')[0]

lines = []
for instance in results.getElementsByTagName('INSTANCE'):
    for prop in instance.getElementsByTagName('PROPERTY'):
        val = prop.getElementsByTagName('VALUE')[0].firstChild.data
    lines.append(val)

text = '\n'.join('start %s & '%line for line in lines)
print(text)
with open('run_mpv.bat', 'w', encoding='cp866') as fh:
    fh.write(text)
