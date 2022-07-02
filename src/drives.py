import subprocess
import xml.dom.minidom
from pprint import pprint


def drives_list():
    cli_command = 'wmic diskdrive get caption,interfacetype,mediatype,model,size /format:rawxml'

    drivelist = subprocess.Popen(cli_command,
                                 shell=True,
                                 stdout=subprocess.PIPE)
    drivelist, err = drivelist.communicate()
    drivelist = drivelist.decode('utf-8', 'ignore')

    doc = xml.dom.minidom.parseString(drivelist)
    results = doc.getElementsByTagName('RESULTS')[0]

    drives = []
    for instance in results.getElementsByTagName('INSTANCE'):
        inst = {}
        for prop in instance.getElementsByTagName('PROPERTY'):
            key = prop.getAttribute('NAME')
            val = prop.getElementsByTagName('VALUE')[0].firstChild.data
            inst[key] = val
        drives.append(inst)

    return drives

pprint(drives_list())
