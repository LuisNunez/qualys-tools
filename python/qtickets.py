
__author__ = "Luis Nunez"
__license__ = "GPLv3"
__version__ = "0.1.20"
__maintainer__ = "Luis Nunez"
__status__ = "Prototype"

import logging
# Logging is configured here becasue qaulysapi include logging.
# Need to look into this issue.
logging.basicConfig(filename='qtickets.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
import qualysapi
from lxml import etree, objectify
from datetime import datetime
import sys

# This script is used to pull Remediation Ticket data from the Qualys
# Guard.

# Connect to Qualys Guard
def QualysConnect(get_state, assignee, last_line_num, file_number):
    Truncation = 1
    file_num = file_number
    while (Truncation == 1):
        print "+ - - - - - - - - - - - - -"
        print "Connecting To QualysGuard"
        logging.info('Connecting To QualysGuard')
        logging.info('Connection %s', file_num)
        print "Connection: %s" % file_num
        #print "Trunction: %s" % Truncation
        qgs=qualysapi.connect()

        # Request data
        if last_line_num == 0:
            print " Intitial get"
            logging.info('Last Line Number: %s', last_line_num)
            logging.info('Get State: %s', get_state)
            ret = qgs.request('ticket_list.php', {'states':get_state, 'ticket_assignee':assignee})
            print "Open out_file %s" % file_num
            snum = str(file_num)
            xmlfile = get_state + snum + ".xml"
            out_file = open(xmlfile, "w")
            print "write to %s" % out_file
            out_file.write(ret)
            print "File Number: %s" % file_num
            #file_num += 1
            print "close %s" % out_file
            out_file.close()
            logging.info('Closed File: ', xmlfile)
        else:
            print "Follow on Since Ticket Number"
            logging.info('Last Line Number: %s', last_line_num)
            #ret = qgs.request('ticket_list.php', {'states':get_state})
            ret = qgs.request('ticket_list.php', {'states':get_state, 'ticket_assignee':assignee, 'since_ticket_number':last_line_num})
            print "last_line_num attribute %s" % last_line_num
            snum = str(file_num)
            xmlfile = get_state + snum + ".xml"
            out_file = open(xmlfile, "w")
            print "write to out_file"
            out_file.write(ret)
            out_file.close()
            print "File Number: %s" % file_num
            logging.info('Closed File: ', xmlfile)

        # XML file processing section.
        print "Process XML file"
        current_datetime = datetime.now()
        print current_datetime
        print "Open XML file for processing"
        print "file name: %s" % xmlfile
        logging.info('Process File: %s', xmlfile)
        with open(xmlfile, 'r') as f:
            xml = f.read()
        #print "file_num before plus1: %s" % file_num
        file_num += 1
        #print "file_num after plus1: %s" % file_num
        root = objectify.fromstring(xml)

        for ticket_line in root.getchildren():
            # print attributes
            # print ticket_line.attrib
            if ticket_line.tag == "TRUNCATION":
                print "Found TRUNCATION"
            # print ticket_line.tag
            # print ticket_line.attrib
                line_num = ticket_line.attrib
                print line_num
                last_line_num = line_num['last']
                print last_line_num
                logging.info('LAST LINE Number: %s', last_line_num)
                Truncation = 1
                #return last_line_num
                #print "For loop Truncation %s: " % Truncation
                logging.info('Trunction found %s', xmlfile)
            elif ticket_line.tag == "ERROR":
                Truncation = 0
                logging.info('Truncation = 0')
                logging.info('ERROR found in %s', xmlfile)
                print "Error found in %s" % xmlfile
                print ticket_line.tag, ticket_line.attrib
            else:
            # print "Truncation Not Found"
                Truncation = 0
                logging.info('Truncation not found %s', xmlfile)
        f.close()

        print "Truncation %s: " % Truncation

def main():
    #logging.basicConfig(filename='qtickets1.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Start Qualys Tickets Script version:%s' % __version__ )
    print "version:", __version__
    # QualysConnect('CLOSED', 0)
    QualysConnect('OPEN', 'username', 0, 1)
    # QualysConnect('RESOLVED', 0)
    # QualysConnect('IGNORED', 2066252)


if __name__ == '__main__':
    main()

