import socket
import ipaddress
import struct
import time

from NetworkLibrary.BaseOperations.BaseIPSocketConnection import BaseIPSocketConnection

from SocketSettings import *

class IPSocketConnection(BaseIPSocketConnection):

    def __init__(self):
        pass

    def ip_create_socket(self, socket_family, socket_type, printer_ip='0.0.0.0', protocol=0, ip_address=socket.gethostbyname(socket.gethostname()), type = transmission_type.unicast):
        """
        Creates socket using the parameters provided. Argument 6 refers to host ip address.

        Arguments: The keyword takes 6 arguments.
        | Argument 1    | Argument 2   | Argument 3  | Argument 4  | Argument 5  | Argument 6  |
        | Socket family | Socket type  | Printer IP  | Protocol    | IP Address  | Type        |

        Example:
        ip_create_socket(socket_family.ipv4, socket_type.udp, '192.168.10.15', socket_protocol.proto_udp, ip_address='192.168.10.20', type=transmission_type.unicast)

        """
        try:
            print '****************Creating Socket Connection****************'
            self.socket_family = int(socket_family)
            self.socket_type = int(socket_type)
            self.socket_protocol = int(protocol)
            self.socket_ip = ip_address
            self.printer_ip = str(printer_ip)
            self.socket = socket.socket(self.socket_family, self.socket_type, self.socket_protocol)

            if type == transmission_type.multicast and self.socket_family == 23:
                hostname = socket.gethostname()
                ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
                client_linklocal = ipv6_list[0][4][0]
                if '%' in client_linklocal:
                    link_local = client_linklocal.split('%')[0]
                self.socket.bind((client_linklocal, 0))
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
                interface_index = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][3]
                multicast_ip = ipaddress.ip_address(self.socket_ip)
                self.socket.setsockopt(41, socket.IPV6_JOIN_GROUP, struct.pack('16sI', multicast_ip.packed, interface_index))
            print '\n\nSocket Created : \nSocket Family ->', self.socket_family, ', \nSocket Type ->', self.socket_type, ', \nProtocol ->', self.socket_protocol, ', \nSocket IP ->', self.socket_ip
            print '\n\n==========================================================================================\n\n\n'
            return self
        except Exception, msg:
            raise AssertionError('Error while creating IP socket: ', msg)

    def ip_listen_socket(self, listen_time , packet_size=2048, is_filter_on=True):
        """
        Listens to the port specified for the mentioned listen time and captures all packets and saves to self.PACKETS as a list. Is filter on filters the packets with source address as printer ip.

        Arguments: The keyword takes 3 arguments.
        | Argument 1  | Argument 2   | Argument 3    |
        | Listen time | Packet Size  | Is filter on  |

        Example:
        ip_listen_socket(60, 4096, False)

        """
        self.captured_packets = []
        time_out = time.time() + int(listen_time)

        self.socket.settimeout(int(listen_time))
        print '****************Socket Listen****************'
        print '\nListening at IP : ', self.socket_ip, ' ...'
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
        print '\n \t No. Packets Received : ', str(len(self.captured_packets))
        print '\n====================================================================================================\n'


    def ip_send_packets(self, packet, destination_ip):
        """
        Sends the packet to the mentioned destination ip and destination port

        Arguments: The keyword takes 2 arguments.
        | Argument 1  | Argument 2      |
        | Packet      | Destination IP  |

        Example:
        ip_send_packets([packet1, packet2,..], '192.168.10.15')

        """
        print '****************Sending Packets****************'
        try:
            for i in range(0, len(packet)):
                log_output = 'RESPONSE PACKET : ' + str(i+1)
                print '+', '-'*len(log_output), '+'
                print '|', ' '*len(log_output), '|', '\tDestination IP :', destination_ip
                print '|', log_output, '|', '\t', '='*25, '>', ' '*10, 'PACKET SENT'
                print '+', '-' * len(log_output), '+\n\n'
                self.socket.sendto(packet[i], (destination_ip, 0))
            print '\n================================================ ===============================================\n'
        except Exception, msg:
            print 'Exception Message: ', msg
            raise AssertionError("Error occured while sending the packets!!: ", msg)

    def ip_close_socket(self):
        """
        Closes the socket connection

        Example:
        ip_close_socket()

        """
        try:
            print '\n\n****************Closing Socket****************'
            self.socket.close()
            print '\n\n\tSocket Closed'
            print '\n================================================================================================\n'
        except:
            raise AssertionError("Error occured while closing the socket! Socket not Closed")
