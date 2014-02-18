#!/usr/bin/env python

import socket
import struct
import select
import time

import multicast_listner_conf

socks = []

def setup_sockets():

	for port in multicast_listner_conf.MCAST_PORTS.keys():
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('', port))
		mreq = struct.pack("4sl", socket.inet_aton(multicast_listner_conf.MCAST_GRP), socket.INADDR_ANY)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
		socks.append(sock)

def setup_select():
	while True:
		print "Waiting for select"
		readable, writable, exceptional = select.select(socks, [], [])
		for sock in readable:
			print sock.recv(1024)

setup_sockets()
setup_select()
