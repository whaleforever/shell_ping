# justping
find the fastest host by ping. input can be feed from command line or file.

## Usage
**justping.py** [ *filename* ] [ **+** ] [ *ip/host* ]...

### Usage
*filename* ------ line based host list to ping. please refer the hosts.txt as sample
**+** ---------------- append host list from command line
*ip/host* -------- ip/hostname

### Examples

* 

        >python justping.py

        ping hosts from hosts.txt

* 

        >python justping.py www.google.com 8.8.8.8

        ping host "www.google.com" and "8.8.8.8"

* 

        >python justping.py local.txt

        ping host list from local.txt
* 

        >python justping.py local.txt + 8.8.8.8

        ping host list from local.txt, and with server 8.8.8.8
