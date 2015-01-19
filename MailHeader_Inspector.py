#!/usr/bin/python

import os
# Find Mail queue size

#print number of folders in directory
####
## We do need to count number of files not number of folders???
####

#def fcount(path):
#  map ={}
#  count = 0
#  for f in os.listdir(path):
#    child = os.path.join(path, f)
#    if os.path.isdir(child):
#      child_count = fcount(child)
#      count += child_count + 1 # unless include self
#  map[path] = count
#  return count

def fcount(path):
	c=0
	for dirpath, dirnames, files in os.walk(path):
    		for name in files:
        		c=c+1
	return c


# Mail Queue size
def queue_size(queue_loc,mta):
	if mta=="Postfix":
		m_queue = ["deferred", "active", "bounce", "corrupt"]
		mail_queue_num = {}
		for i in m_queue:
			mail_queue_num[i] = fcount(queue_loc+i)
		#print mail_queue_num
		#deferred_mails = fcount(queue_loc+"deferred")
		#active_mails = fcount(queue_loc+"active")
		#bounced_mails = fcount(queue_loc+"bounce")
		#corrupt_mails = fcount(queue_loc+"corrupt")
		#total_mails = deferred_mails + active_mails + bounced_mails + corrupt_mails
		print "Total Messages: ", mail_queue_num['bounce']+ mail_queue_num['deferred']+mail_queue_num['active']+mail_queue_num['corrupt']
		print "Bounced Mail Queue :", mail_queue_num['bounce']
		print "Deffered Mail Queue :", mail_queue_num['deferred']
		print "Active Mail Queue :", mail_queue_num['active']
		print "Corrupt Mail Queue:", mail_queue_num['corrupt']

	elif mta=="Qmail":
		m_queue = ["remote", "local", "bounce"]
                mail_queue_num = {}
                for i in m_queue:
                        mail_queue_num[i] = fcount(queue_loc+i)
		print "Total Messages: ", mail_queue_num['remote']+ mail_queue_num['local']+mail_queue_num['bounce']
                print "Bounced Mail Queue :", mail_queue_num['bounce']
                print "Deffered Mail Queue :", mail_queue_num['remote']
                print "Active Mail Queue :", mail_queue_num['local']
	else:
		print "MTA running on this server is not supported by this script"

		
#path = "/var/spool/postfix/test"

		
#print fcount(path)

queue_size("/var/spool/postfix/","Postfix") 

#print fcount("/var/spool/postfix/test/")
#topdir = '/var/spool/postfix/test/'

#print folderCount
# Find mail with lots of receipent


# Read a mail header

# Read a mail with content

