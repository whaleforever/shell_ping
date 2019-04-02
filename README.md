# shell ping
## Usage
**shell_ping(hostname, times=4, timeout=5)**

#### params
*hostname* : host or ip to ping (e.g www.google.com, 192.168.1.1)<br/>
*times* : retries<br/>
*timeout* : seconds before timeout

#### results
* ip: ip address
* time_min: time minimum
* time_avg: time average
* time_max: time maximum lost in ms
