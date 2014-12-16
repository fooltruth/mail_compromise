#!/usr/bin/python
import subprocess,sys,platform

class EnvironmentDiscovery:
	def __init__(self):
		pass   

        # identify PHP version
	def php_version(self):
		php_ver = "php -v | egrep PHP.\s*[0-9]\.[0-9] | awk '{print $2}'"
		p = subprocess.Popen(php_ver, stdout=subprocess.PIPE, shell=True)
		output, err = p.communicate()
		return output	

	def is_plesk(self):
		plesk_process = "netstat -ntpl | grep 'sw-cp-server' | wc -l"
		p = subprocess.Popen(plesk_process, stdout=subprocess.PIPE, shell=True)
		output, err = p.communicate()
		if int(output) >= 1:
			return True
		else: 
			return False
	
	def mta_f(self,x):
		return {
			'master': 'Postfix',
			'xinetd': 'Qmail',
			'sendmail': 'Sendmail',
			'exim': 'Exim',
		}.get(x,'Unknown')

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

	
	def linux_dist(self):
		return platform.dist()
