#!/usr/bin/env python
""" find the fastest host from file by ping
"""

import re
import os
import sys
import shell_ping


def get_hosts(filename):
    """ get IP/hostname from file
    return IP/hostname list, default is null
    """
    hosts = []
    with open(filename) as f:
        for line in f:
            line = line.strip().strip('.,/')
            if line:
                hosts.append(line)
    return hosts

if __name__ == '__main__':
    argvs = sys.argv
    hosts = []
    filename = 'hosts.txt'
    append = False
    result_time = {}

    if len(argvs) >= 2:
        target = argvs[1]

        if os.path.isfile(target):
            filename = target

            if leng > 2:
                if argvs[2] == '+':
                    append = True
                    target = argvs[3:]
                else:
                    target = argvs[2:]
        elif target == '+':
            append = True
            target = argvs[2:]
        else:
            target = argvs[1:]
        if target:
            for s in target:
                name = s.strip('.,/')
                name = re.sub(r'https?://', '', name)
                hosts.append(name)

    if not hosts:
        # read from file and remove duplicates
        hosts = list(set(get_hosts(filename)))
    else:
        # remove duplicates
        hosts = list(set(hosts))
        # append additional host from command line
        if append:
            hosts = list(set(get_hosts(filename) + hosts))

    if not hosts:
        sys.exit('No host to ping.')

    print 'host(ip)'.rjust(34), ' min_time'.rjust(8), 'avg_time'.rjust(8), 'max_time'.rjust(8), 'lost'.rjust(8)

    for x in hosts:
        ip, time_min, time_avg, time_max, lost = shell_ping.ping(x, times=5)
        result_time.update({x: [time_min, time_avg, time_max]})
        print ('%s(%s): ' % (x, ip)).rjust(35),\
              ('% 3sms' % (time_min)).rjust(8),\
              ('% 3sms' % (time_avg)).rjust(8),\
              ('% 3sms' % (time_max)).rjust(8),\
              ('% 2s%%' % (lost)).rjust(8)

    times = sorted(result_time.itervalues())
    # remove no reaching results
    times = [i[0] for i in times[:] if i[0] > 0]

    if times:
        for k, v in result_time.iteritems():
            if v[0] == times[0]:
                print '%s has min ping time: %s ms' % (k, v[0])
