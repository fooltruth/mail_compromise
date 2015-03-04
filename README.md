SpamSpotter
============

SpamSpotter is a script written in python which allows users to identify the source of outgoing spam on a linux server. This script also verifies whether 
the IP address of a server is blacklisted and if the 3-way DNS check is satisfied.

Compatability:

- Linux based OS
- PHP 5.3 and above
- python 2.4 and above


<h3>Download/Installation</h3>

Users can download the entire repository by using 'git clone' followed by the cloning URL above. Alternatively, use the following:

wget https://raw.githubusercontent.com/fooltruth/mail_compromise/master/SpamIdentifier.py -O SpamIdentifier.py
python SpamIdentifier.py

The execute bit (chmod +x SpamIdentifier.py) can be added so that the script can be executed without calling python directly.

<h3>Application Usage</h3>

Here are instructions for Basic Usage of this script:

SpamIdentifier.py -a 

Run SpamIdentifier.py -h for a full list of available flags and operations


