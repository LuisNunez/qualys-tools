# This code parses Qualys Host Detect scan data(XML)
# This variation parses QID 38116 SSL Server Information Retrieval.
# QID 38116 provides checks to see if the SSL and TLS enabled.
# 
# version 0.1.0
# prototype 

import sys 
import csv
from lxml import etree, objectify
from sys import argv


def parseXML(xmlFile):
    #""" test """
    csvfile = open('test_csv.csv','w')
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    with open(xmlFile) as f:
        xml = f.read()
 
    root = objectify.fromstring(xml)
 
    # returns attributes in element node as dict
    attrib = root.attrib
 
    # how to extract element data
    #begin = root.RESPONSE.HOST_LIST.HOST
    #uid = root.RESPONSE.DATETIME
    
    #print begin
    SSLTLS = ["TLS", "SSLv2", "SSLv3"]
    SSLTLS_out = []
    # loop over elements and print their tags and text
    for appt in root.RESPONSE.HOST_LIST.getchildren():
        for e in appt.getchildren():
            if e.tag == "IP":
                #ip_e = e.text.rstrip('\n')
                #print ", %s" % e.text
                ip_e = e.text
                #sys.stdout.write(e.text + ", ")
            if e.tag == "OS":
                #print ", %s" % e.text
                #sys.stdout.write(e.text + ", ")
                #os_e = e.text.rstrip('\n')
                #print ", %s" % os_e
                os_e = e.text
            #print "%s => %s" % (e.tag, e.text)
            if e.tag == "DNS":
                #print ", %s" % e.text
                #sys.stdout.write(e.text + ", ")
                dns_e = e.text
            if e.tag == "LAST_SCAN_DATETIME":
                #print "%s => %s" % (e.tag, e.text)
                #print "%s" % e.text
                #sys.stdout.write(e.text + ", ")
                scan_date = e.text
            for ee in e.getchildren():
                #if ee.tag == "IP":
                #print "%s => %s" % (ee.tag, ee.text)
                for eee in ee.getchildren():
                    if eee.tag == "RESULTS":
                        #results_eee = eee.text.replace('\n',', ')
                        #results_x = results_eee.replace('\t',' ')
                        #print "%s\r" % results_x
                        #print "%s\r" % eee.text
                        #sys.stdout.write(eee.text)
                        results = eee.text
                        results_split = results.split('\n')
                        for x in results_split:
                            if 'SSLv3' in x:
                                SSLTLS_out.append(x)
                            elif 'SSLv2' in x:
                                SSLTLS_out.append(x)
                            elif 'TLS' in x:
                                SSLTLS_out.append(x)
                        #print SSLTLS_out

        #print "---------------------------------"
        sys.stdout.write(scan_date + ", " + ip_e + ", " + os_e + ", " + dns_e + ", ")
        
        results_csv = []
        for z in SSLTLS_out:
            results_eee = z.replace('\n',', ')
            results_x = results_eee.replace('\t','')
            sys.stdout.write(results_x + ", ")
            results_csv.append(results_x)
        sys.stdout.write("\n")
        writer.writerow((scan_date, ip_e, os_e, dns_e, results_csv))
        #writer.writerow((results_csv))

        SSLTLS_out = []
    csvfile.close()
#----------------------------------------------------------------------
if __name__ == "__main__":
    #f = r'38116.xml'
    f = argv[1]
    parseXML(f) 