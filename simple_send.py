import socket
import sys

if len(sys.argv) == 3:
	port = int(sys.argv[1])
	message = sys.argv[2]
else:
	port = 10000
	message = 'no message'

grp = '224.1.1.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto(message, (grp,port))
