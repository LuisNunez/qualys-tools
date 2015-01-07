# Python script for parsing and cleaning a Qualys report
__author__ = "Luis Nunez"
__license__ = "GPLv3"
__version__ = "1.6.1"
__maintainer__ = "Luis Nunez"
__status__ = "Prototype"


# Library dependencies
# csv       - is for CSV manipulation
# datetime  - is for generating timestamp
# os        - is to retrieve file stats (size)
# sys       - is used to pass arguments
# argparse  - is used for passing arguments and help menu. Replacement for sys argv.
# copy      - is used for copying the divion, region, and country sting into a new variable.

# CSV Filer Cleaner class needed for blank line in CSV files.
class CSVFileCleaner:
    def __init__(self, file_to_wrap, comment_starts = ('#', '//', '-- ')):
        self.wrapped_file = file_to_wrap
        self.comment_starts = comment_starts
    def next(self):
        line = self.wrapped_file.next()
        while line.strip().startswith(self.comment_starts) or len(line.strip())==0:
            line = self.wrapped_file.next()
        return line
    def __iter__(self):
        return self


import csv
import datetime
import os
import sys
import argparse
import copy

# csv field size to accommodate large field lenghts.
csv.field_size_limit(3500000)


def main():
    parser = argparse.ArgumentParser(description = "Python Qualys CSV Parse script version 1.6.0")
    parser.add_argument('filename')
    parser.add_argument("-s", "--skiplines", dest = 'skiplines', action='store', default= 8, type=int, help='Default is 8. Number of intial lines to skip during processing.')
    args = parser.parse_args()

    print "Qualys Split Script 1.6.1\n"
    # Get Start time of the script
    start_time = datetime.datetime.now().isoformat()
    print "Start Time: %s" % start_time

    file_stat = os.stat(args.filename)
    script_log = open('qualys_csv_split.log', 'a')
    script_log.write(start_time)
    script_log.write('-Start Time-\n')

    print "Opening %s (%dKB)\n" % (args.filename, file_stat.st_size)
    xread = csv.reader(CSVFileCleaner(open(args.filename)))

    # Variables
    count_line = 2
    count_line_outfile = 0
    count_line_outfile1 = 0

    String_1 = "No vulnerabilities match your filters for these hosts"
    String_2 = "No results available for these hosts"

    outfile_path = 'out/'+args.filename
    outfile = open(outfile_path, 'w')
    a = csv.writer(outfile, quoting=csv.QUOTE_ALL)

    # get header section
    print "Line: 1 -- Parse First Line for report Division, Country and Region and Timestamp"
    first_line = xread.next()
    #print first_line
    # Convert first_line list into string.
    s = str(first_line)
    # Write to log file Country, Region and timestamp information.
    script_log.write(s)
    title = first_line[0]
    title_split = title.split('_')
    division = title_split[0]
    region = title_split[1]
    country = title_split[2]

    report_timestamp = first_line[1]
    report_timestamp_split = report_timestamp.split(' ')
    report_timestamp_date = report_timestamp_split[0]
    report_timestamp_time = report_timestamp_split[2]
    print "Report timestamp: %s:%s" % (report_timestamp_date, report_timestamp_time)
    print "Divsion, Region, Country -- %s : %s : %s" % (division, region, country)

    list_of_strings = ['No vulnerabilities match your filters for these hosts', 'No results available for these hosts']

    for x in xread:
        if String_1 in x:
        #if x in list_of_strings:
            print "Found On Line: %s String1:'%s' " % (count_line, String_1) 
            count_line += 1
        elif String_2 in x:
            print "\nFound On Line: %s String2:'%s' " % (count_line, String_2)
            count_line += 1
        elif count_line < args.skiplines:
            print "skip line: %s" % count_line
            count_line += 1
        else:
            w = copy.copy(x)
            # Following pop removes the results column.
            #w.pop(29)
            w.append(division)
            w.append(region)
            w.append(country)
            w.append(report_timestamp_date)
            w.append(report_timestamp_time)
            a.writerow(w)
            print "Line:\r%d" % count_line,
            count_line += 1
    
    print "\nWrote %d lines to %s" % (count_line, outfile_path)
    print "\n\nClosed outfile"

    script_log.write('\t-Read file:%s\n' % args.filename)
    report_time = datetime.datetime.now().isoformat()
    print "Start Time:\t%s" % start_time
    print "End time:\t%s\n" % report_time

    script_log.write(report_time)
    script_log.write('-End time-\n')

    print "Total lines processed: %d\n" % count_line
    print "End script"

    # Close open files.
    outfile.close()
    script_log.close()

if __name__ == '__main__':
    main()
