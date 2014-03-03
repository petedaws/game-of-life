import sys
import socket
import event
import struct
import conf

class MessageRx(event.Event):
	
	def __init__(self,port=10000):
		event.Event.__init__(self)
		self.__create_socket()

	def __create_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', conf.message_bus_port))
		mreq = struct.pack("4sl", socket.inet_aton(conf.message_bus_grp), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self):
		data = self.sock.recv(2048)
		message = eval(data)
		if validate_message(message):
			self.emit('new_message',message)

class MessageTx(event.Event):
	
	def __init__(self,port=10000):
		event.Event.__init__(self)
		self.__create_socket()

	def __create_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', conf.message_bus_port))
		mreq = struct.pack("4sl", socket.inet_aton(conf.message_bus_grp), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def transmit(self,data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.sendto(str(data), (conf.message_bus_grp, conf.message_bus_port))

def validate_message(message):
	if type(message) is not dict:
		raise Exception("ERROR: invalid message - not a dictionary")
	valid_key = int
	valid_value = dict
	key,value = message.iteritems().next()
	if type(key) is not valid_key:
		raise Exception("ERROR: invalid message - No Entity ID")
	if type(value) is not valid_value:
		raise Exception("ERROR: invalid message - No Attributes")
	if validate_attributes(value):
		return True			

def validate_attributes(attributes):
	for key,value in attributes.iteritems():
		if key not in attributes:
			raise Exception("ERROR: invalid message - missing data item")
		if not type(attributes[key]) == valid_attributes[key]:
			raise Exception("ERROR: invalid message - incorrect type for %s" % (key))
	return True	

valid_attributes = {
			'position_x':float,
			'position_y':float,
			'type':str,
			'state':str,
			'age':float,
			'max_age':float,
			'age_rate':float,
			'food':float,
			'reproduce_food':float,
			'max_speed':float,
			'behaviour':str,
			}
		
