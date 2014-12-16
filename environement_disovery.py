import platform
import sys
import subprocess
import os
def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

print("""Python version: %s
dist: %s
linux_distribution: %s
system: %s
machine: %s
platform: %s
uname: %s
version: %s
""" % (
sys.version.split('\n'),
str(platform.dist()),
linux_distribution(),
platform.system(),
platform.machine(),
platform.platform(),
platform.uname(),
platform.version(),
))

mta_process_id = "netstat -ntpl | grep 25 | awk -F/ '{print $2}' | uniq"
mta_processes = "netstat -ntpl | grep 25 | awk -F/ '{print $2}' | uniq | wc -l"
p1 = subprocess.Popen(mta_process_id, stdout=subprocess.PIPE, shell=True)
#p1 = subprocess.Popen(['netstat', '-ntpl'], stdout=subprocess.PIPE) 
#p2 = subprocess.Popen(['grep', '25'], stdin=p1.stdout)
#p3 = subprocess.Popen(['awk', '{print $7}'],stdin=p2.stdout)
#output, err = p2.communicate()
outputp1, err = p1.communicate()

p2 = subprocess.Popen(mta_processes, stdout=subprocess.PIPE, shell=True)
outputp2, err = p2.communicate()

def mta_f(x):
	return {
		'master': 'Postfix',
		'xinetd': 'Qmail',
		'sendmail': 'Sendmail',
		'exim': 'Exim',
	}.get(x,'Unknown')

if int(outputp2) == 1:
        outputp1 = outputp1.rstrip()	
	mta = mta_f(outputp1)
        print mta
elif int(outputp2) == 0:
	print "No mail service is currently running. Please start mail service and run the script again."
else:
	print "There are multiple MTA's running and this script is not compatiable"



php_ver = "php -v | egrep PHP.\s.*[0-9]\.[0-9] | awk '{print $2}'"
p3 = subprocess.Popen(php_ver, stdout=subprocess.PIPE, shell=True)
outputp3, err = p3.communicate()

print outputp3

plesk_process = "netstat -ntpl | grep 'sw-cp-server' | wc -l"
p4 = subprocess.Popen(plesk_process, stdout=subprocess.PIPE, shell=True)
outputp4, err = p4.communicate()
plesk = False
if int(outputp4) >= 1:
	plesk = True
else: 
	plesk = False


print plesk
