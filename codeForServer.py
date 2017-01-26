import urllib2, socket

IP = socket.gethostbyname(socket.getfqdn())

urllib2.urlopen("http://jmanyc123:flybabyfly@dynupdate.no-ip.com/nic/update?hostname=flybabyfly.ddns.net&myip=" + IP).read()

## Hostname: flybabyfly.ddns.net