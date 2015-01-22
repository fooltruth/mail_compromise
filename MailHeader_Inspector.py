#!/usr/bin/python

import os, random,subprocess,re
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

		
queue_size("/var/spool/postfix/","Postfix") 

# Get a specified number mail headers from specififed queue
def getRandMailHeaders(queue,n):
	for dirpath, dirnames, files in os.walk(queue):
		if len(files)>=n:
                	return random.sample(files,n)
		else:
			return files

# Read a mail
def viewMail(mid,mta):
	if mta=="Postfix":
		read_mail = "postcat -q " + mid
	elif mta=="Qmail":
		read_mail = "find /var/qmail/queue/mess/ -name" + mid
        p = subprocess.Popen(read_mail, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        return output
	
#print viewMail("3B77413C1B3")

#Get a list of line of lines contains a specific word
def grepfunc(text,pattern):
	l = []
	for i in text.split('\n'):
                if re.search(pattern,i):
                        for w in i.split(" "):
                                l.append(w)
			l.append('\n')
        return l


# Idetify if the mail was sent via PHP script or from Mail authentication
def mailOrigin(mid,mta):
	#mail = viewMail(mid,mta)
	f = open('/var/spool/postfix/deferred/3/3A77414C1B3','r')
	mail = f.read()
	f.close()
	if mta=="Postfix":
		if grepfunc(mail,"Received")[-2:-1][0][:-1]==110:	
			print "Auth User"
		else:
			print "PHP Script"

	elif mta=="Qmail":
		qmail_list=grepfunc(mail,"Received: \(qmail")
		for i in qmail_list:
			if re.search("network",i):	
				print "Auth User"
			else: 
				print "PHP Script"

	
mailOrigin("3B77413C1B3","Postfix")


#print folderCount
# Find mail with lots of receipent


# Read a mail header

# Read a mail with content

