#!/usr/bin/python

import fileinput
import sys
import re
from collections import defaultdict

class MailParser:
	# Read X number of lines of maillog file from bottom. "tail" like function 
	def tail(self,f, lines=5000):
    		total_lines_wanted = lines

    		BLOCK_SIZE = 1024
    		f.seek(0, 2)
    		block_end_byte = f.tell()
    		lines_to_go = total_lines_wanted
    		block_number = -1
    		blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    		while lines_to_go > 0 and block_end_byte > 0:
        		if (block_end_byte - BLOCK_SIZE > 0):
            			# read the last block we haven't yet read
            			f.seek(block_number*BLOCK_SIZE, 2)
            			blocks.append(f.read(BLOCK_SIZE))
        		else:
            			# file too small, start from begining
            			f.seek(0,0)
            			# only read what was not read
            			blocks.append(f.read(block_end_byte))
        		lines_found = blocks[-1].count('\n')
        		lines_to_go -= lines_found
        		block_end_byte -= BLOCK_SIZE
        		block_number -= 1
    		all_read_text = ''.join(reversed(blocks))
	    	return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])



	# Get list of email address authenticated with IPs
	def auth_email_list(self,maillog_loc,pattern,pos1,pos2):
		fo = open(maillog_loc, "r")
		file = self.tail(fo)
		auth_emails=defaultdict(list)
		for i in file.split('\n'):
			if re.search(pattern,i):
				l = []
                		for w in i.split(" "):
					l.append(w) 
				auth_emails[l[pos1]].append(l[pos2])
        	fo.close()
		return auth_emails
		#print auth_emails['alex@slpy.com']	

#auth_email_list("/var/log/alexlog","logged in")
