#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file implement the TCPPortScanner class. """

###################
#    This file implement the TCPPortScanner class.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

import socket
from time import sleep

class TCPPortScanner:

	""" This class configure and launch a TCP connect scan. """

	def __init__ (self, target, ports = range(1,1024), timeout = 0.5, with_handle = True, inter = 0):
		self.target = target
		self.ports = ports
		self.with_handle = with_handle
		self.timeout = timeout
		self.inter = inter

		if not with_handle:
			self.opened_ports = []

	def test_port (self, port):

		""" This function try to established a connection. """

		try:
			socket.create_connection((self.target, port), timeout = self.timeout)
		except TimeoutError:
			pass
		except socket.timeout:
			pass
		except ConnectionRefusedError:
			pass
		except OSError:
			pass
		else:
			if self.with_handle:
				self.handle(port)
			else:
				self.opened_ports.append(port)

	def handle (self, port):

		""" To get a port in real time. """

		print(f"open: {port}")

	def scan (self):

		""" Main function to scan. """

		for port in self.ports:
			if self.inter:
				sleep(self.inter)
			self.test_port(port)

if __name__ == "__main__":
	scanner = TCPPortScanner("192.168.0.254", (53,80,443,445,5000), with_handle = False)
	scanner.scan()
	print(scanner.opened_ports)

	scanner = TCPPortScanner("192.168.0.254")
	scanner.scan()