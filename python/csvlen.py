#
# csvlen.py
# Script looks for large fields in CSV files.

# CSV Filer Cleaner class need for blank line in CSV files.
class CSVFileCleaner:
    def __init__ (self, file_to_wrap, comment_starts=('#', '//', '-- ')):
        self.wrapped_file = file_to_wrap
        self.comment_starts = comment_starts
    def next (self):
        line = self.wrapped_file.next()
        while line.strip().startswith(self.comment_starts) or len(line.strip())==0:
            line = self.wrapped_file.next()
        return line
    def __iter__ (self):
        return self


import csv
import datetime
import os
from sys import argv


def main(test_file):
	#xlarge = 31073
	xlarge = 20000
	size_up = 331073
	line_count = 0
	large_line_count = 0
	csv.field_size_limit(size_up)
	xread = csv.reader(CSVFileCleaner(open(test_file)) )
	for x in xread:
		line_count += 1
		#print "Line:%s" % line_count
		for z in x:
			w=len(z)
			#print z, w
			if w > xlarge:
				print "GREATER Than %s" % xlarge
				print "Line:%s" % line_count
				#print z
				large_line_count += 1
			else:
				pass
				#print "LESS Than %s" % xlarge
	print "\ntotal large fields:%s over %s characters" % (large_line_count,xlarge)

			

if __name__ == '__main__':
	main(argv[1])