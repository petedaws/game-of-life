import socket

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 30010

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto("blah_de_blah_blah", (MCAST_GRP, MCAST_PORT))
