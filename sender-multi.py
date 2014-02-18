#!/usr/bin/env python

import socket

import multicast_listner_conf
for port in multicast_listner_conf.MCAST_PORTS.keys():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	sock.sendto(multicast_listner_conf.MCAST_PORTS[port], (multicast_listner_conf.MCAST_GRP, port))
