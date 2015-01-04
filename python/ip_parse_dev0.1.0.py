# Open a CSV file, read and printout file contents
# Search and find and convert IP ranges 
# version 0.1.0


import csv

count_lines = 0
count_range = 0
count_diff_octet = 0
count_x = 0
# met_assetgroup_list.csv

with open('file.csv','r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		Asset_Group_Title = row[0]
		Asset_Group = row[1]
		
		x = Asset_Group_Title.find('*')
		if x == 0:
			count_x += 1 
		# Find a '-' in the row.  Detect a range entrAsset_Group_IP.
		z = Asset_Group.find('-')
		
		# If '-' is detected parse and split out to string.
		if z > 1:
			# Split the to IP address between the '-'.
			Asset_Group_IP = Asset_Group.split('-')
			# split out the IP Address
			IP_a = Asset_Group_IP[0]
			IP_b = Asset_Group_IP[1]
			# Further split the IP address into octects
			aa = IP_a.split('.')
			bb = IP_b.split('.')

			# Convert from string to integer
			aaa = int(aa[3])
			bbb = int(bb[3])
			aaa3 = int(aa[2])
			bbb3 = int(bb[2])

			if aaa3 != bbb3:
				# Process third octet
				third_Octec_diff = (bbb3) - aaa3
				if third_Octec_diff < 0:
					print "Line Numbe: %s" % count_lines
					print "found negitive number"
				if aaa3 < bbb3:
					for k in range(aaa3, bbb3):
						kk = str(k)
						# print "%s.%s.%d.0/24"% (aa[0], aa[1], k)
						# Form the octets into an IP address
						form_ip = aa[0]+'.'+ aa[1] + '.' + kk + '.' + '0/24'
						print row[0], form_ip	
					#print "-------------------"
					print "Line Number: %s" % count_lines
					print "Subnets"
					print "AGI %s range is from %s to %s" % (row[0], IP_a, IP_b)
					print "There are %s subnets in the range" % third_Octec_diff
					print "-------------------"
					count_diff_octet += 1
				elif aaa3 > bbb3:
					print "Octet a is higher than Octet b"
					for k in range(third_Octec_diff, aaa3):
						kk = str(k)
						# print "%s.%s.%d.0/24"% (aa[0], aa[1], k)
						# Form the octets into an IP address
						form_ip = aa[0]+'.'+ aa[1] + '.' + kk + '.' + '0/24'
						print row[0], form_ip	
					
					print "Line Number: %s" % count_lines
					print "Subnets"
					print "AGI %s range is from %s to %s" % (row[0], IP_a, IP_b)
					print "There are %s subnets in the range" % third_Octec_diff
					#print "-------------------"
					count_diff_octet += 1
			elif aaa == 0 or 1 and bbb == 254 or 255:
				print row[0] + ', ' + IP_b + '/24'
				print "Summerized IP"
				print "AGI %s range is %s to %s" % (row[0], IP_a, IP_b)
				print "-------------------"
			elif aaa == bbb:
				# Process fourth octet
				r = bbb - aaa
				for k in range(aaa, bbb):
						kk = str(k)
						# print "%s.%s.%d.0/24"% (aa[0], aa[1], k)
						# Form the octets into an IP address
						form_ip = aa[0]+'.'+ aa[1] + '.' + aa[2] + '.' + kk+'/32'
						print row[0] + ', ' + form_ip	
				print row[0] + ', ' + IP_b + '/32'
				print "Line Number: %s" % count_lines
				print "IP Host"

				#print "-------------------"
				print "AGI %s range is %s to %s" % (row[0], IP_a, IP_b)
				print "There are %s in the range" % r
				print "-------------------"
				count_range += 1
		count_lines += 1

# Calculate total host lines (single IP address)
count_host_lines =  count_lines - (count_range + count_diff_octet)

print "Total lines: %s" % count_lines
print "Total lines with ranges: %s" % count_range
print "Total lines with multiple subnets: %s" % count_diff_octet
print "Total lines with single IP: %s" % count_host_lines
print "Total x: %s" % count_x

# Close file
csvfile.close