#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file implement the PortsScanner class. """

###################
#    This file implement the PortsScanner class.
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

__all__ = [ "PortsScanner", "main" ]

from argparse import ArgumentParser
from time import perf_counter, sleep

class PortsScanner :

    """ This class configure and launch the port scan. """

    def __init__ (self, target, ports = { 
            80 : "http",
            53 : "domain",
            139 : "netbios_ssn",
            137 : "netbios_ns",
            445 : "microsoft_ds",
            443 : "https", 
            21 : "ftp", 
            22 : "ftps", 
            110 : "pop3",
            995 : "pop3 ssl",
            143 : "imap",
            993 : "imap ssl",
            25 : "smtp",
            465 : "smtp ssl",
            587 : "smtp ssl",
            3306 : "MySQL",
            2082 : "cPanel",
            2083 : "cPanel ssl",
            2086 : "WebHostManager",
            2087 : "WebHostManager ssl",
            2095 : "Webmail",
            2096 : "Webmail ssl",
            2077 : "WebDAV/WebDisk",
            2078 : "WebDAV/WebDisk ssl" },
            timeout : float = 0,
            inter : float = 0,
            retry : int = 1,
            flags : str = None,
            type_ : str = "default",
            timer : bool = False,
            flags_response : str = "SA",
            view_real_time : bool = True,
            invers : bool = False,
            timeout_total : int = 100,
            workers : int = 500,
            unanswers : bool = False,
            probability_min : int = 100):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.inter = inter
        self.retry = retry or 1
        self.timer = timer
        self.type = type_
        self.flags_response = flags_response
        self.view_real_time = view_real_time
        self.invers = invers
        self.time = None
        self.timeout_total = timeout_total
        self.workers = workers
        self.unanswers = unanswers
        self.probability_min = probability_min

        if not self.view_real_time:
            self.opened_ports = []

        if invers:
            self.set_invers()

        self.flags = flags
        self.TCP_SERVICES = self.get_tcp_services()

    def set_invers (self):

        """ Configure inversed scan. """

        self.invers = True
        self.opened_ports = list(self.ports)
        self.ports = self.opened_ports.copy()
        self.view_real_time = False
        self.unanswers = False

    def start_timer (self):

        """ Get start time for timer. """

        if self.timer:
            self.start = perf_counter()

    def stop_timer (self) -> float:

        """ Get stop time for timer and return interval with start time. """

        if self.timer:
            self.stop = perf_counter()
            return self.stop - self.start

    def udp_socket_scan (self, payload=b"\0", size=1024):
        sock = self.socket.socket(family=self.socket.AF_INET, type=self.socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        for port in self.ports:
            try:
                sock.sendto(payload, (self.target, port))
                sock.recvfrom(size)
            except self.socket.timeout:
                self.handle_find_port(port)
            except ConnectionResetError:
                sleep(self.inter)

    def udp_scan_ (self):

        """ UDP scan with scapy sr function. """

        self.responses, self.unanswers = self.sr(self.IP(dst=self.target)/self.UDP(dport=[port for port in self.ports]), inter=self.inter, timeout=self.timeout, verbose=1)

        for packet in self.unanswers:
            self.handle_find_port(packet[self.UDP].dport)

    def udp_scan (self):

        """ UDP with scapy AsyncSniffer. """

        sniffer = self.AsyncSniffer(
            lfilter=lambda response: (response.haslayer(self.UDPerror) and 
                response.getlayer(self.IP) and 
                response.getlayer(self.IP).src==self.target),
            prn=lambda packet: self.handle_find_port(packet.getlayer(self.UDPerror).dport))
        sniffer.start()

        self.send(self.IP(dst=self.target)/self.UDP(dport=self.ports), inter = self.inter, verbose=0)

        sleep(self.timeout)
        sniffer.stop()

    def launcher (self):

        """ Method to launch scan. """

        if self.type == "S":
            scan = self.scan_SYN()
        elif self.type == "F":
            scan = self.scan_FIN()
        elif self.type == "X":
            scan = self.scan_XMAS()
        elif self.type == "N":
            scan = self.scan_NULL()
        elif self.type == "A":
            scan = self.scan_ACK()
        elif self.type == "U":
            scan = self.scan_UDP()
        else:
            scan = self.requirements()

        self.start_timer()
        for a in range(self.retry):
            scan()
        self.time = self.stop_timer()

    def requirements (self):

        """ This function check requirement for scan and find the better alternative when you don't have the requirement. """

        SCAPY = False

        # if self.type == "U" and self.view_real_time:
        #     try:
        #         from scapy.all import AsyncSniffer, send, IP, UDP, UDPerror
        #     except ModuleNotFoundError:
        #         SCAPY = False
        #         print("Scapy ins't install...\n"
        #             "This UDP scan is longest than UDP Scapy scan.")
        #     else:
        #         SCAPY = True

        #         self.AsyncSniffer = AsyncSniffer
        #         self.send = send
        #         self.IP = IP
        #         self.UDPerror = UDPerror
        #         self.UDP = UDP

        #         self.set_invers()

        #         return self.udp_scan

        if self.type == "U" and not self.view_real_time:
            try:
                from scapy.all import IP, sr, UDP
            except ModuleNotFoundError:
                SCAPY = False
                print("Scapy ins't install...\n"
                    "This UDP scan is longest than UDP Scapy scan.")
            else:
                SCAPY = True

                self.sr = sr
                self.IP = IP
                self.UDP = UDP

                return self.udp_scan_

        if self.type == "U" and not SCAPY:
            import socket
            self.socket = socket
            return self.udp_socket_scan

        if (self.flags or self.type == "N") and (self.type != "async" and self.type != "connect"):
            try:
                from scapy.all import AsyncSniffer, send, IP, TCP, sr
            except ModuleNotFoundError:
                SCAPY = True
                print("Scapy isn't install...\n"
                    "The scan type become async or connect.")
            else:
                SCAPY = False

                self.AsyncSniffer = AsyncSniffer
                self.send = send
                self.IP = IP
                self.TCP = TCP
                self.sr = sr

                return self.tcp_scan

        if ((self.type == "default" or SCAPY == False) and not self.inter) or self.type == "async":
            from .TCPAsyncPortScanner import TCPAsyncPortScanner
            from asyncio import run

            self.TCPAsyncPortScanner = TCPAsyncPortScanner
            self.run = run
            self.type = "async"

            return self.scan_TCP_async

        elif ((self.type == "default" or SCAPY == False) and self.inter) or self.type == "connect":
            from .TCPPortScanner import TCPPortScanner

            self.TCPPortScanner = TCPPortScanner
            self.type = "connect"

            return self.scan_TCP_connect

    def scan_SYN (self):

        """ This function configure SYN scan. """

        self.flags = "S"
        self.flags_response = "SA"
        self.invers = False
        self.unanswers = False
        return self.requirements()

    def scan_FIN (self):

        """ This function configure FIN scan. """

        self.flags = "F"
        self.flags_response = "RA"
        self.unanswers = True
        self.view_real_time = False
        self.opened_ports = []
        return self.requirements()

    def scan_NULL (self):

        """ This function configure NULL scan. """

        self.flags = ""
        self.flags_response = "RA"
        self.unanswers = True
        self.view_real_time = False
        self.opened_ports = []
        return self.requirements()

    def scan_XMAS (self):

        """ This function configure Xmas tree scan (flags : FPU). """

        self.flags = "FPU"
        self.flags_response = "RA"
        self.unanswers = True
        self.view_real_time = False
        self.opened_ports = []
        return self.requirements()

    def scan_ACK (self):

        """ This function configure ACK scan. """

        self.flags = "A"
        self.flags_response = "R"
        self.unanswers = True
        self.view_real_time = False
        self.opened_ports = []
        return self.requirements()

    def scan_UDP (self):

        """ This function configure UDP scan. """

        self.unanswers = True
        self.view_real_time = False
        self.opened_ports = []
        self.timeout = 3
        return self.requirements()

    def tcp_scan (self):

        """ Launch TCP scans. This function implement a scapy TCP scan with sr function. """

        if self.view_real_time:
            self.tcp_scan_realtime()
            return

        self.responses, self.unanswers = self.sr(self.IP(dst=self.target)/self.TCP(flags=self.flags, dport=self.ports), 
            timeout = self.timeout if self.timeout else 3, verbose = 1, inter = self.inter)

        if self.unanswers:
            for packet in self.unanswers:
                self.handle_find_port(packet.getlayer(self.TCP).dport)
        else:
            for packet in self.responses:
                tcp = packet[1].getlayer(self.TCP)
                if tcp and tcp.flags == self.flags_response:
                    self.handle_find_port(tcp.sport)

    def handle_find_port (self, port):

        """ Function to get port in real time. """

        if self.view_real_time:
            print(f"open: {port} "
                f"{self.ports[port] if isinstance(self.ports, dict) and port in self.ports.keys() else ''}"
                f" {self.TCP_SERVICES[port] if port in self.TCP_SERVICES else ''}")
        elif self.invers and not self.unanswers:
            self.opened_ports.remove(port)
        else:
            self.opened_ports.append(port)

    def tcp_scan_realtime (self):

        """ This method implement tcp scan with scapy AsyncSniffer. """

        if isinstance(self.ports, dict):
            ports = [port for port in self.ports]
        else:
            ports = self.ports

        sniffer = self.AsyncSniffer(
            lfilter=lambda response: (response.haslayer(self.TCP) and 
                response.getlayer(self.IP) and 
                response.getlayer(self.IP).src==self.target and 
                response.getlayer(self.TCP).flags==self.flags_response),
            prn=lambda packet: self.handle_find_port(packet.getlayer(self.TCP).sport))
        sniffer.start()

        self.send(self.IP(dst=self.target)/self.TCP(dport=ports, flags=self.flags), inter = self.inter, verbose=0)

        sleep(self.timeout or 3)
        sniffer.stop()

    def scan_TCP_connect (self):

        """ This method launch a TCP connect scan. """

        scanner = self.TCPPortScanner(self.target, self.ports, self.timeout or 0.5, self.view_real_time, self.inter)
        scanner.scan()

        if not self.view_real_time:
            self.opened_ports = scanner.opened_ports

    def scan_TCP_async (self):

        """ This method launch a TCP asynchronous scan. """

        scanner = self.TCPAsyncPortScanner(self.target, self.ports, self.timeout or 3, self.workers, self.timeout_total, self.view_real_time)
        self.run(scanner.scan())

        if not self.view_real_time:
            self.opened_ports = scanner.opened_ports

    def report_from_port (self, port):

        """ This function return a opened port report. """

        result = ""
        probability = self.opened_ports.count(port) / self.retry * 100

        result += (f"open: {port} "
                        f"{self.ports[port] if isinstance(self.ports, dict) and port in self.ports.keys() else ''}"
                        f" {self.TCP_SERVICES[port] if port in self.TCP_SERVICES else ''}")

        if self.probability_min != 100 and probability >= self.probability_min:
            result += f" {probability}%"
        elif probability < self.probability_min:
            return
        return result

    def report (self):

        """ This function print a scan report. """

        if not self.view_real_time:

            result = {}
            for port in self.opened_ports:
                port_report = self.report_from_port(port)
                if not result.get(port) and port_report:
                    result[port] = port_report

            print("\n".join(result.values()))

            if not len(self.opened_ports):
                print("No result : Some reasons : This computer may be protect"
                    " by firewall or this computer doesn't have opened ports or if"
                    " this scan is a async scan you have to high number of workers.")
            elif len(self.opened_ports) > 2500:
                print("The scan result is highest than 2500 opened ports : Possible"
                    " reasons : this scan need a interval between requests.")

        if self.time:
            print(f"Report for {self.target} with scan type : \"{self.type}\".")
            print(f"Scanned in {self.time} seconds.")

    def get_tcp_services (self) -> dict:

        """ This function return services by ports. """

        try:
            from scapy.all import TCP_SERVICES
        except ModuleNotFoundError:
            from socket import getservbyport

            TCP_SERVICES = {}
            #for port in range(65536): # execution time ~= 300 seconds
            #    try:
            #        TCP_SERVICES[port] = getservbyport(port)
            #    except OSError:
            #        pass
        
        return TCP_SERVICES

def parse ():

    """ Parse arguments. """

    parser = ArgumentParser()

    parser.add_argument("target", help="IP or hostname to scan.")
    parser.add_argument("--ports", "-p", help="List of port to scan or range of ports to scan.")
    parser.add_argument("--timeout", "-t", help="Time to wait a response.", type=float, default=0)
    parser.add_argument("--inter", "-i", help="Time between sending packets.", type=float, default=0)
    parser.add_argument("--retry", "-r", help="Relaunch scan to get a better fiability.", type=int, default=1)
    parser.add_argument("--flags", "-f", help="For custom flags on TCP scan.", default=None)
    parser.add_argument("--flags_responses", "-F", help="For custom flags responses on TCP scan.", default="RA")
    parser.add_argument("--type", "-T", help="To use an implement scan.", default="default", choices=("S","F","X","N","A","U","async","connect","default"))
    parser.add_argument("--timer", help="Calcul and print the execution time.", action="store_true")
    parser.add_argument("--result-in-real-time", "-R", help="Print result in real time.", action="store_true")
    parser.add_argument("--invers", "-I", help="Invers the result to get unanswered ports.", action="store_true")
    parser.add_argument("--timeout-total", "-q", help="Second to stop scan [for async scan].", type=int, default=100)
    parser.add_argument("--workers", "-w", help="Number of async workers.", type=int, default=500)
    parser.add_argument("--unanswers", "-u", help="Get only the unanswered ports.", action="store_true")
    parser.add_argument("--probability-minimum", "-m", help="The minimum probability (in pourcent) to add port in report.", type=int, default=100)

    return parser.parse_args()

def get_ports (string_ports):

    """ Get ports generator from string. """

    from re import finditer, match
    ports = []

    for range_ in finditer("[0-9]{1,5}[-][0-9]{1,5}", string_ports):
        range_ = range_.group()
        range_ = range_.split("-")
        ports.append(range(int(range_[0]), int(range_[1]) + 1))

    simple_ports = []
    for port in string_ports.split(","):
        port = match("^[0-9]{1,5}$", port)
        if port:
            simple_ports.append(int(port.group()))

    ports.append(simple_ports)
    ports = [port for ports in ports for port in ports]

    return ports

def main ():
    parser = parse()

    if parser.ports:
        ports = get_ports(parser.ports)

        scanner = PortsScanner(parser.target, ports, parser.timeout, parser.inter, parser.retry, parser.flags, parser.type, parser.timer, parser.flags_responses, parser.result_in_real_time, parser.invers, parser.timeout_total, parser.workers, parser.unanswers, parser.probability_minimum)
    else:
        scanner = PortsScanner(parser.target, timeout=parser.timeout, inter=parser.inter, retry=parser.retry, flags=parser.flags, type_=parser.type, timer=parser.timer, flags_response=parser.flags_responses, view_real_time=parser.result_in_real_time, invers=parser.invers, timeout_total=parser.timeout_total, workers=parser.workers, unanswers=parser.unanswers, probability_min=parser.probability_minimum)

    scanner.launcher()
    scanner.report()
    
if __name__ == "__main__":
    ports = get_ports("80")

    compteur = 0
    for port in ports:
        assert port == 80
        compteur += 1

    assert compteur == 1

    ports = get_ports("80,443")

    compteur = 0
    for port in ports:
        assert port == 80 or port == 443
        compteur += 1

    assert compteur == 2

    ports = get_ports("443-446")

    compteur = 0
    for port in ports:
        assert port >= 443 and port <= 446
        compteur += 1

    assert compteur == len(range(443, 447))

    ports = get_ports("80,443-446")

    compteur = 0
    for port in ports:
        assert (port >= 443 and port <= 446) or port == 80
        compteur += 1

    assert compteur == len(range(443, 447)) + 1

    ports = get_ports("53-80,443-446")

    compteur = 0
    for port in ports:
        assert (port >= 443 and port <= 446) or (port >= 53 and port <= 80)
        compteur += 1

    assert compteur == len(range(443, 447)) + len(range(53, 81))

    main()