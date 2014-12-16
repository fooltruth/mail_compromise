import platform
import sys
import subprocess

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

p1 = subprocess.Popen(["netstat", "-ntpl"], stdout=subprocess.PIPE) 
p2 = subprocess.Popen(["grep", "25"], stdin=p1.stdout)
p3 = subprocess.Popen([],stdin=p2.stdout)
output, err = p2.communicate()
print output

