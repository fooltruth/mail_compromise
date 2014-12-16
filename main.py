#!/usr/bin/python
from Environment_Discovery import EnvironmentDiscovery

e = EnvironmentDiscovery()
print e.php_version()
print e.is_plesk()
e.mta_type()
print e.linux_dist()
