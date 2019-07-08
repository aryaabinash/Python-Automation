import socket
import sys
import time
import struct
import ipaddress
from SocketSettings import *
from NetworkLibrary.BaseOperations.BaseUDPSocketConnection import BaseUDPSocketConnection



class UDPSocketConnection(BaseUDPSocketConnection):


    def __init__(self):
        self.captured_packets = []

    def udp_create_socket(self, socket_family, socket_type, port, printer_ip='0.0.0.0', protocol=17, ip_address=socket.gethostbyname(socket.gethostname()), type = transmission_type.unicast):
        """
        Creates socket using the parameters provided. Argument 6 refers to host ip address.
        
        Arguments: The keyword takes 7 arguments.
        | Argument 1    | Argument 2   | Argument 3  | Argument 4  | Argument 5  | Argument 6  | Argument 7  |
        | Socket family | Socket type  | Port        | Printer IP  | Protocol    | IP Address  | Type        |

        Example:
        udp_create_socket(socket_family.ipv4, socket_type.udp, 67, '192.168.10.15', socket_protocol.proto_udp, ip_address='192.168.10.20', type=transmission_type.unicast)

        """
        try:
            print '****************Creating Socket Connection****************'
            self.socket_family = int(socket_family)
            self.socket_type = int(socket_type)
            self.socket_port = int(port)
            self.socket_protocol = int(protocol)
            self.socket_ip = str(ip_address)
            self.printer_ip = str(printer_ip)
            self.socket = socket.socket(self.socket_family, self.socket_type, self.socket_protocol)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            if type == transmission_type.unicast:
                self.socket.bind((ip_address, self.socket_port))
            elif self.socket_ip == '' or type == transmission_type.broadcast:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.socket.bind(('', self.socket_port))
            elif type == transmission_type.multicast and self.socket_family == 23:
                #multicast_ip = unicode(self.SOCKET_IP, 'utf-8')
                multicast_ip = self.socket_ip.decode('utf-8')
                print 'unicode address: ', multicast_ip
                address = ipaddress.ip_address(multicast_ip)
                print address
                interface_index = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][3]
                print 'interface index: ', interface_index
                print 'ip: ', ip_address
                print 'port: ',port
                link_local = 'fe80::e8c3:6c0d:cf3a:aa72'
                hostname = socket.gethostname()
                ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
                client_linklocal = ipv6_list[0][4][0]
                if '%' in client_linklocal:
                    link_local = client_linklocal.split('%')[0]
                interface_index = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][3]
                self.socket.bind((link_local, self.socket_port))
                self.socket.setsockopt(41, socket.IPV6_JOIN_GROUP, struct.pack('16sI', address.packed, interface_index))
            elif type == transmission_type.multicast and self.socket_family == 2:
                self.socket.bind(('', self.socket_port))
                client_ip = socket.gethostbyname(socket.gethostname())
                mreq = socket.inet_aton(self.socket_ip) + socket.inet_aton(client_ip)
                self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, str(mreq))

            print '\n\nSocket Created : \nSocket Family ->', self.socket_family, ', \nSocket Type ->', self.socket_type, ', \nPort ->', self.socket_port, ', \nProtocol ->', self.socket_protocol, ', \nSocket IP ->', self.socket_ip
            print '\n\n==========================================================================================\n\n\n'
            return self
        except Exception, msg:
            raise AssertionError('Error while creating UDP socket: ', msg)

    def udp_listen_socket(self, listen_time, packet_size=2048, is_filter_on = True):
        """
        Listens to the port specified for the mentioned listen time and captures all packets and saves to self.PACKETS as a list. Is filter on filters the packets with source address as printer ip.

        Arguments: The keyword takes 3 arguments.
        | Argument 1  | Argument 2   | Argument 3    |
        | Listen time | Packet Size  | Is filter on  |

        Example:
        udp_listen_socket(60, 4096, False)

        """
        self.captured_packets = []
        time_out = time.time() + int(listen_time)

        self.socket.settimeout(int(listen_time))
        print '****************Socket Listen****************'
        print '\nListening at Port :', self.socket_port, ' , IP : ', self.socket_ip, ' ...'
        print '\n Time out value :', listen_time, ' seconds'
        count = 0
        while time.time() < time_out:
            try:
                packet_data, source_ip = self.socket.recvfrom(int(packet_size))
                # print 'sourceip: ', source_ip
                # print 'packet data: ', packet_data
                if is_filter_on:
                    if self.printer_ip in source_ip[0]:
                        packet = [packet_data, source_ip]
                        self.captured_packets.append(packet)
                else:
                    packet = [packet_data, source_ip]
                    self.captured_packets.append(packet)
            except socket.timeout:
                print '\n\n Timed Out!!! No more packets on network to capture. Closing Socket\n'
        print '\n \t No. Packets Received : ', len(self.captured_packets)
        print '\n====================================================================================================\n'

    def udp_send_packets(self, packet, destination_ip, destination_port):
        """
        Sends the packet to the mentioned destination ip and destination port

        Arguments: The keyword takes 3 arguments.
        | Argument 1  | Argument 2      | Argument 3        |
        | Packet      | Destination IP  | Destination Port  |

        Example:
        udp_send_packets([packet1, packet2,..], '192.168.10.15', 1234)

        """
        print '****************Sending Packets****************'
        try:
            for i in range(0, len(packet)):
                log_output = 'RESPONSE PACKET : ' + str(i+1)
                print '+', '-'*len(log_output), '+'
                print '|', ' '*len(log_output), '|', '\tDestination IP :', destination_ip
                print '|', log_output, '|', '\t', '='*25, '>', ' '*10, 'PACKET SENT'
                print '|', ' '*len(log_output), '|', '\tDestination Port : ', destination_port
                print '+', '-' * len(log_output), '+\n\n'
                self.socket.sendto(packet[i], (destination_ip, int(destination_port)))
            print '\n================================================ ===============================================\n'
        except Exception, msg:
            print 'Exception Message: ', msg
            raise AssertionError("Error occured while sending the packets!!")

    def udp_close_socket(self):
        """
        Closes the socket connection

        Example:
        udp_close_socket()

        """
        try:
            print '\n\n****************Closing Socket****************'
            self.socket.close()
            print '\n\n\tSocket Closed on port ', self.socket_port
            print '\n================================================================================================\n'
        except:
            raise AssertionError("Error occured while closing the socket! Socket not Closed")
