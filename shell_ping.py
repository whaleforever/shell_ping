"""
The MIT License (MIT)

Copyright (c) 2019 whaleforever, rogers0

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import os
import re
import subprocess

def ping(target, times=4, timeout=5):
    """ ping target in IP/hostname format
    params:
        target:
            e.g.
                '192.168.1.1' or 'www.google.com'
        times: times to retries ping command
        timeout: in seconds to stop ping command

    return ip, time_min, time_avg, time_max, lost in ms
        ip: IP address of target, default is 0.0.0.0
        time_min: min ping time(ms), default is -1
        time_avg: avg ping time(ms), default is -1
        time_max: max ping time(ms), default is -1
        lost: packet loss(%), default is 100

        ('www.google.com', '127.0.0.1', 5, 0)
    """

    if os.name == 'nt':  # win32
        cmd = 'ping -w %d '%(timeout * 1000) + target
    else:  # unix/linux
        cmd = 'ping -c%d -W%s %s' % (times, timeout, target)

    # execute ping command and get stdin thru pipe
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
    if not pipe:
        return '0.0.0.0', -1, -1, -1, 100

    # replace CR/LF
    text = pipe.decode().replace('\r\n', '\n').replace('\r', '\n')

    # match IP address in format: [192.168.1.1] (192.168.1.1)
    ip = re.findall(r'(?<=\(|\[)\d+\.\d+\.\d+\.\d+(?=\)|\])', text)
    if ip:
        ip = ip[0]
    else:
        ip = re.findall(r'\d+\.\d+\.\d+\.\d+', text)
        ip = ip[0] if ip else '0.0.0.0'

    # avg ping time
    if os.name == 'nt':
        time = re.findall(r'(\d+(?=ms))+', text)
        if time:
          time_avg = float(time[len(time) - 1])
          time_max = float(time[len(time) - 2])
          time_min = float(time[len(time) - 3])
    else:
        time = re.findall(r'(?=\d+\.\d+/)(\d+\.\d+)+', text)
        if time:
          time_min = float(time[0])
          time_avg = float(time[1])
          time_max = float(time[2])
    if not time:
       time_min = time_avg = time_max = -1

    # packet loss rate
    lost = re.findall(r'\d+.\d+(?=%)', text)
    if not lost:
        lost = re.findall(r'\d+(?=%)', text)
    lost = int(round(float(lost[len(lost)-1]))) if lost else 100

    return ip, time_min, time_avg, time_max, lost
