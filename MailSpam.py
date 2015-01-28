#!/usr/bin/python

import os,random,subprocess,re,time,datetime,platform

spam_keywords=['sex','Vigara','Viigara' ,'aDult','Debt','already approved', 'already wealthy', 'amazing new discovery', 'amazing pranks', 'an excite game', 'and you save','nasty','babe','fuck']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# This class discovers all required feature of environement
# * OS distribution
# * PLesk or Non Plesk
# * MTA Type
# * PHP version
class EnvironmentDiscovery:
	# Empty constructor 
	def __init__(self):
		pass   

        # identify PHP version
	def php_version(self):
		php_ver = "php -v | egrep PHP.\s*[0-9]\.[0-9] | awk '{print $2}'"
		p = subprocess.Popen(php_ver, stdout=subprocess.PIPE, shell=True)
		output, err = p.communicate()
		return output	

	# Is it a plesk server?
	def is_plesk(self):
		plesk_process = "netstat -ntpl | grep 'sw-cp-server' | wc -l"
		p = subprocess.Popen(plesk_process, stdout=subprocess.PIPE, shell=True)
		output, err = p.communicate()
		if int(output) >= 1:
			return True
		else: 
			return False
	
	# matches keyword again MTAs
	def mta_f(self,x):
		return {
			'master': 'Postfix',
			'xinetd': 'Qmail',
			'sendmail': 'Sendmail',
			'exim': 'Exim',
		}.get(x,'Unknown')


	# Discover MTA using netstat output. 
	def mta_type(self):
		mta_process_id = "netstat -ntpl | grep :25 | awk -F/ '{print $2}' | uniq"
		mta_processes = "netstat -ntpl | grep :25 | awk -F/ '{print $2}' | uniq | wc -l"
		p1 = subprocess.Popen(mta_process_id, stdout=subprocess.PIPE, shell=True)
		outputp1, err = p1.communicate()

		p2 = subprocess.Popen(mta_processes, stdout=subprocess.PIPE, shell=True)
		outputp2, err = p2.communicate()

		if int(outputp2) == 1:
        		outputp1 = outputp1.rstrip()	
			mta = self.mta_f(outputp1)
        		#print mta
			return mta
		elif int(outputp2) == 0:
			print "No mail service is currently running. Please start mail service and run the script again."
		else:
			print "There are multiple MTA's running and this script is not compatiable"

	# Find Linux Distribution and version	
	def linux_dist(self):
		return platform.linux_distribution()

	# Determine mail log path based on environment
        def mail_log_path(self,distro,plesk):
		Redhat = set(['Redhat','CentOS'])
        	Debian = set(['Ubuntu','Debian'])

		if plesk:
			return "/usr/local/psa/var/log/maillog"
		elif distro in Redhat:
			return "/var/log/maillog"
		elif distro in Debian:
			return "/var/log/mail.log"
		else: 
			return "Unknown"

	def mail_queue_loc(self,mta):
		if mta=="Postfix":
			return "/var/spool/postfix/"
		elif mta=="Qmail":
			return "/var/qmail/queue/"
		else: 
			return "Not Supported"

#e = EnvironmentDiscovery()
#MTA=e.mta_type()
#print "Mail Service is: ", MTA
#print "Plesk server? ", e.is_plesk()
#print e.mail_log_path(e.linux_dist()[0],e.is_plesk())
#MAILLOG_PATH=e.mail_log_path(e.linux_dist()[0],e.is_plesk())
#print MAILLOG_PATH

#MAIL_QUEUE_LOC=e.mail_queue_loc(MTA)
#print MAIL_QUEUE_LOC


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

def intersection(iterableA, iterableB, key=lambda x: x):
    """Return the intersection of two iterables with respect to `key` function.

    """
    def unify(iterable):
        d = {}
        for item in iterable:
            d.setdefault(key(item), []).append(item)
        return d

    A, B = unify(iterableA), unify(iterableB)

    return [(A[k], B[k]) for k in A if k in B]


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
		print "\n"
	elif mta=="Qmail":
		m_queue = ["remote", "local", "bounce"]
                mail_queue_num = {}
                for i in m_queue:
                        mail_queue_num[i] = fcount(queue_loc+i)
		print "Total Messages: ", mail_queue_num['remote']+ mail_queue_num['local']+mail_queue_num['bounce']
                print "Bounced Mail Queue :", mail_queue_num['bounce']
                print "Deffered Mail Queue :", mail_queue_num['remote']
                print "Active Mail Queue :", mail_queue_num['local']
		print "\n"
	else:
		print "MTA running on this server is not supported by this script"

		
#queue_size(MAIL_QUEUE_LOC,MTA) 

# Get a specified number mail headers from specififed queue
def getRandMailHeaders(queue,n):
	f_list = []
	for dirpath, dirnames, files in os.walk(queue):
		for name in files:
			f_list.append(name)
	if len(f_list)>=n:
               	return random.sample(f_list,n)
	else:
		return f_list

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
def mailOrigin(mail,mta):
	# Postfix: Examine the last "Recived: by" line. Bounced emails with have more than one "Received: by" lines.
        # Last entry on the line indicates the userid. If userid is 110, mail is generated from Auth users. 
        # This is only true for Plesk servers. 
	if mta=="Postfix":
		if grepfunc(mail,"Received: by")[-2:-1][0][:-1]==110:	
			return "Auth"
		else:
			return "PHP"
	# Qmail: Examine the last "Recived:" line. Bounced emails with have more than one "Received:" lines.
        # If the received line contains an entry "network", mail is generated from Auth users; Otherwise from PHP script 
	elif mta=="Qmail":
		qmail_list=grepfunc(mail,"Received: \(qmail")
		for i in qmail_list:
			if re.search("network",i):	
				return "Auth"
			else: 
				return "PHP"

	
#mailOrigin("3B77413C1B3","Postfix")


def isSpamMail(mid,mta):
	mail = viewMail(mid,mta)
	#print mail
  	#f = open('/var/spool/postfix/deferred/3/3A77414C1B3','r')
        #mail = f.read()
        #f.close()
	
	if mailOrigin(mail,mta)=="PHP":
		if (len(intersection(spam_keywords, grepfunc(mail,"Subject:"), key=str.lower)) > 0): 
			return "spam",grepfunc(mail,"X-PHP-Originating-Script")[1].split(':')[1]
		elif (len(grepfunc(mail,"X-PHP-Originating-Script"))>0):
			return "possible",grepfunc(mail,"X-PHP-Originating-Script")[1].split(':')[1]
		else:
			return "enable","Enable PHP add_x_header"
	else:
		return "auth","Auth"		

#print isSpam("3A77414C1B3","Postfix")	

def isSpam(queue,mta):
	def_spam = []
	pos_spam = []
	for i in getRandMailHeaders(queue,5):
		print isSpamMail(i,mta)[0]
		if isSpamMail(i,mta)[0]=="spam":
			def_spam.append(isSpamMail(i,mta)[1])
		elif isSpamMail(i,mta)[0]=="possible":
                	pos_spam.append(isSpamMail(i,mta)[1])
		else:
			print "No SPAM!!!!!"
       #### If queue is less than 2?????
        ###
	if len(def_spam) > 2:
		return "Spam", def_spam
	elif len(pos_spam) > 2:
		return "possible", pos_spam
	else:
		return "Select another 5"

def find_php_file(path,fname):
	cmd = "find " +path+ " -name " +fname+ " -type f"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        return output


## if 0 return then file is infected; 1 file is not infected; 2 - file is not there
def isInfected(fname):
        cmd = "egrep 'passthru|shell_exec|base64_decode|edoced_46esab' "  + fname
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
        output, err = p.communicate()
        return p.returncode


def verifySpam(mta):
	if mta=="Postfix":
		queue = "/var/spool/postfix/deferred"
	elif mta=="Qmail":
		queue = "/var/qmail/queue/mess"
	else:
		"Unsupported Mail Service"

	path = "/var/www/"

	n = 5
	d_file = []
	if isSpam(queue,mta)[0]=="Spam":
		#print f_list
		f_list = set(isSpam(queue,mta)[1])
		for i in f_list:
			for j in find_php_file(path,i).split('\n'):
				d_file.append(j)
	elif isSpam(queue,mta)[0]=="possible":
		f_list = set(isSpam(queue,mta)[1])
                for i in f_list:
                        for j in find_php_file(path,i).split('\n'):
				d_file.append(j)  
	#print d_file
	for key in d_file:
		if isInfected(key)==0:
			f_timestamp=datetime.datetime.fromtimestamp(os.path.getmtime(key))
			if (datetime.datetime.now() - f_timestamp) < datetime.timedelta(days=2):
				print "Infected file is: " + key
				return True
			else:
				print "Infected file is: " +key
				return True 				
		elif isInfected(key)==1:
			f_timestamp=datetime.datetime.fromtimestamp(os.path.getmtime(key))	
			if (datetime.datetime.now() - f_timestamp) < datetime.timedelta(days=2):
				print "File was modified with in 2 days, most likly spam sent from thisi : " + key
			else:
				print "Manually verify this file: " + key
			return False 				
			
		else:
			print "Nothing to be done"
			return False




e = EnvironmentDiscovery()
MTA=e.mta_type()
PHP_VERSION=e.php_version()
if (MTA=="Postfix") or (MTA=="Qmail"):
	print "\n"
	print "*************************"
	print "Plesk server? ", e.is_plesk()
	print "*************************"
	print "\n"
	print "*************************"
	print bcolors.BOLD + "Mail Service is: ", MTA, "" + bcolors.ENDC
	print "*************************"

	#print e.mail_log_path(e.linux_dist()[0],e.is_plesk())
	MAILLOG_PATH=e.mail_log_path(e.linux_dist()[0],e.is_plesk())
	print MAILLOG_PATH
	MAIL_QUEUE_LOC=e.mail_queue_loc(MTA)
	print MAIL_QUEUE_LOC

	#m=MailParser()
	#m.auth_email_list(MAILLOG_PATH,)

	queue_size(MAIL_QUEUE_LOC,MTA)
	if float(PHP_VERSION[0:3]) >= 5.3:
		for i in range(3):
			if verifySpam(MTA)==True:
				break
	else:
		print bcolors.FAIL + "PHP version is:", PHP_VERSION, "PHP 5.3 and above is required to identify the spam file. Please refere to the following article to identify the script manaually. " +bcolors.ENDC

#isSpam("/var/spool/postfix/deferred","Postfix")
#verifySpam(MTA)		
#print folderCount
# Find mail with lots of receipent


# Read a mail header

# Read a mail with content

