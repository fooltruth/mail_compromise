#!/usr/bin/python
import subprocess,platform

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
		mta_process_id = "netstat -ntpl | grep 25 | awk -F/ '{print $2}' | uniq"
		mta_processes = "netstat -ntpl | grep 25 | awk -F/ '{print $2}' | uniq | wc -l"
		p1 = subprocess.Popen(mta_process_id, stdout=subprocess.PIPE, shell=True)
		outputp1, err = p1.communicate()

		p2 = subprocess.Popen(mta_processes, stdout=subprocess.PIPE, shell=True)
		outputp2, err = p2.communicate()

		if int(outputp2) == 1:
        		outputp1 = outputp1.rstrip()	
			mta = self.mta_f(outputp1)
        		print mta
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
		
