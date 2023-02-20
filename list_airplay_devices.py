#!/usr/bin/env python3
from zeroconf import Zeroconf, ServiceBrowser

class MyListener:
	def remove_service(self, zeroconf, type, name):
		print(f"Service {name} removed")

	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		if info and b"_airplay._tcp.local." in info.type:
			print(f"AirPlay device found: {name.decode('utf-8')} at {info.addresses[0]}:{info.port}")

zeroconf=Zeroconf()
listener=MyListener()
browser=ServiceBrowser(zeroconf, "_services._dns-sd._udp.local.", listener)

try:
	input("Press enter to exit...\n\n")
finally:
	zeroconf.close()