import socket

class socket_family:
    ipv4 = socket.AF_INET
    ipv6 = socket.AF_INET6

class socket_type:
    tcp = socket.SOCK_STREAM
    udp = socket.SOCK_DGRAM
    raw = socket.SOCK_RAW

class socket_protocol:
    proto_tcp = socket.IPPROTO_TCP
    proto_udp = socket.IPPROTO_UDP
    proto_ip = socket.IPPROTO_IP
    proto_icmp = socket.IPPROTO_ICMP
    proto_raw = socket.IPPROTO_RAW

class transmission_type:
    unicast = 'unicast'
    broadcast = 'broadcast'
    multicast = 'multicast'

class WSPrintPackets:
    subscription_packet = ''
    subscription_event = ''


