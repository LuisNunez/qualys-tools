# Parse and print out Qualys QIDs 
__author__ = "Luis Nunez"

__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Luis Nunez"
__status__ = "Prototype"

import re
import csv
import copy
import xml.etree.ElementTree as ET


outfile = open('met_asset.csv', 'wb')

tree = ET.parse('host.xml')
root = tree.getroot()

hl = root.find('RESPONSE/HOST_LIST')
host_count = 0
Info_count = 0
Conf_count = 0
Poten_count = 0
outfile_count = 0

for elem in list(hl):
    #print elem
    host_count += 1
    host_id = elem.find('ID')
    host_ip = elem.find('IP')
    host_dns = elem.find('DNS')
    last_scan_datetime = elem.find('LAST_SCAN_DATETIME')
    det_tags = elem.find('DETECTION_LIST')

    # det_tag[0] - QID
    # det_tag[1] - TYPE
    # det_tag[2] - 

    for det_tag in list(det_tags):
        if det_tag[1].text == "Info":
            #print '--Info'
            #print '%s, %s, %s' % (host_id.text, det_tag[1].text, det_tag[0].text)
            #print "%s=\"%s\"" % (det_tag.tag,det_tag[1].text)
            Info_count += 1
            if det_tag[0].text == '90235':
                print "--90235--"
                x = det_tag[2].text
                xx = re.split(r'\n+', x)
                for y in xx:
                    #print y
                    z = re.split(r'\t+', y)
                    #print host_id.text, host_ip.text, host_dns.text, z[0], z[1]
                    asset_row = host_id.text +', '+ host_ip.text + ', ' + host_dns.text +', ' + z[0] + ', ' + z[1]+'\n'
                    # Encode to ASCII for file write.  Discovered data had UTF8 in data.
                    asset_row_string = asset_row.encode('ascii', 'ignore')
                    print asset_row
                    outfile.write(asset_row_string)
                    outfile_count += 1
                    # print outfile_count
                #print "---------"
        elif det_tag[1].text == "Confirmed":
            #print '%s, %s, %s' % (host_id.text, det_tag[1].text, det_tag[0].text)
            Conf_count += 1
        elif det_tag[1].text == "Potential":
            #print '%s, %s, %s' % (host_id.text, det_tag[1].text, det_tag[0].text)
            Poten_count += 1

print "\n\nHost Count: %s" % host_count
print "Informational Count: %s" % Info_count
print "Confirmed Count: %s" % Conf_count
print "Potential Count: %s" % Poten_count


