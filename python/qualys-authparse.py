# This code parses Qualys Host Detect scan data(XML)
# version 0.1.0
# prototype 

from lxml import etree, objectify
 
#----------------------------------------------------------------------
def parseXML(xmlFile):
    """"""
    with open(xmlFile) as f:
        xml = f.read()
 
    root = objectify.fromstring(xml)
 
    # returns attributes in element node as dict
    attrib = root.attrib
 
    # how to extract element data
    begin = root.RESPONSE.HOST_LIST.HOST
    uid = root.RESPONSE.DATETIME
    
    print begin
    
    # loop over elements and print their tags and text
    for appt in root.RESPONSE.HOST_LIST.getchildren():
        for e in appt.getchildren():
            if e.tag == "LAST_SCAN_DATETIME":
                #print "%s => %s" % (e.tag, e.text)
                print "%s" % e.text
            if e.tag == "IP":
                print ", %s" % e.text
            if e.tag == "DNS":
                print ", %s" % e.text
            #print "%s => %s" % (e.tag, e.text)
            for ee in e.getchildren():
                #if ee.tag == "IP":
                    #print "%s => %s" % (ee.tag, ee.text)
                for eee in ee.getchildren():
                    if eee.tag == "RESULTS":
                        print ", %s" % eee.text
            #print "%s >> %s" % (e.ID, e.text)
        #for e in appt.ID():
        #    print "%s => %s" % (e.tag, e.text)
        #print
 
    # how to change an element's text
    #root.appointment.begin = "something else"
    #print root.appointment.begin
 
    # how to add a new element
    #root.appointment.new_element = "new data"
 
    # print the xml
    obj_xml = etree.tostring(root, pretty_print=True)
    #print obj_xml
 
    # remove the py:pytype stuff
    objectify.deannotate(root,cleanup_namespaces=True)
    #etree.strip_attributes(root, '{http://www.w3.org/2001/XMLSchema-instance}nil')
    etree.cleanup_namespaces(root)
    obj_xml = etree.tostring(root, pretty_print=True)
    #print obj_xml
 
    # save your xml
    #with open("new.xml", "w") as f:
    #    f.write(obj_xml)
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    f = r'WinAuth105015.xml'
    parseXML(f) 