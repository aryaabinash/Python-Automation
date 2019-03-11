from Packages.Socket.SocketSettings import *
import socket
import time

class TCPSocketConnection:

    def __init__(self):
        # m = WSPrintValidation()
        self.PACKETS = []

    def tcp_create_connection(self, IP_ADDRESS, port, socket_family =''):
        """
        Creates scoket using the parameters provided
        :param socket_family: ipv4/ipv6
        :param port: port number the socket need be binded
        :param IP_ADDRESS: Printer ip / client ip
        :return: NIL
        """
        print '*****************************Creating Socket Connection*************************************************'
        if socket_family == 'ipv6':
            socket_family =socket.AF_INET6
        else:
            socket_family = socket.AF_INET
        self.SOCKET_PORT = int(port)
        self.IP_ADDRESS = str(IP_ADDRESS)
        self.SOCKET = socket.socket(socket_family, socket.SOCK_STREAM)
       # print '\n\nSocket Created : \nSocket Family ->', self.SOCKET_FAMILY, ', \nSocket Type ->', self.SOCKET_TYPE, ', \nPort ->', self.SOCKET_PORT, ', \nProtocol ->', self.SOCKET_PROTOCOL, ', \nSocket IP ->', self.SOCKET_IP
        print '\nSocket Created : \nPrinter IP ->', self.IP_ADDRESS, ' \nPort ->', self.SOCKET_PORT
        print '========================================================================================================'
        return self

    def tcp_connect_connection(self):
        try:
            self.SOCKET.connect((self.IP_ADDRESS, self.SOCKET_PORT))
        except:
            raise AssertionError ("Error occured while connect!!")


    def tcp_send_packets(self, packet):
        """
        Sends the packet to the mentioned destination ip and destination port
        :param packet:  Packet to be sent
        :return: NIL
        """
        print '********************************Sending Packets*********************************************************'
        try:
            # print packet
            self.SOCKET.send(packet)
            print "\t\t Packet sent successfully"
            print '===================================================================================================='
        except:
            raise AssertionError("Error occured while sending the packets!!")

    def tcp_close_connection(self):
        """
        Closes the socket connection
        :return: NIL
        """
        try:
            print '\n********************************Closing Socket****************************************************'
            self.SOCKET.close()
            print '\n\tSocket Closed'
            print '===================================================================================================='
        except:
            raise AssertionError("Error occured while closing the socket! Socket not Closed")

    def tcp_receive_packets(self, size = 10000):
        print '********************************Receiving Packets***************************************************'
        try:
            self.SOCKET.shutdown(socket.SHUT_WR)
            received_packet = self.SOCKET.recv(size)
            print '\n Response Packet received successfully'
            return received_packet
        except:
            raise AssertionError("Error occurred while receiving the socket! Socket not received")

    def tcp_listen_packets(self,time_out=300):
        print '********************************listening Packets***************************************************'
        self.SOCKET.bind((self.IP_ADDRESS, self.SOCKET_PORT))
        self.SOCKET.setblocking(0)
        self.SOCKET.settimeout(time_out)
        self.SOCKET.listen(1)
        time_out = time.time() + time_out
        try:
            while time.time() < time_out:
                clientsocket, addr = self.SOCKET.accept()
                time.sleep(4)
                clrec = clientsocket.recv(2000)
                self.PACKETS.append(clrec)
        except socket.timeout:
            pass
        except Exception, msg:
            raise AssertionError("Unable to listen packets in port 5357 -> %s" % msg)