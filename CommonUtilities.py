import uuid
import binascii
import socket

from uuid import getnode as get_mac


class CommonUtilities:
    def __init__(self):
        pass

    def random_uuid(self):
        """
        reading random uuid

        """
        try:
            uuid_value = uuid.uuid4()
            return str(uuid_value)
        except:
            raise AssertionError('Unable to generate UUID')

    # -----------------------------------GET HOSTNAME--------------------------------------------#
    def get_client_hostname(self):
        hostname = socket.gethostname()
        return hostname

    # -----------------------------------GET IPV4 address-----------------------------------------------#
    def get_client_ipv4(self):
        hostname = socket.gethostname()
        client_ipv4 = socket.gethostbyname(hostname)
        return client_ipv4

    # -----------------------------------GET LINK LOCAL IPv6 address--------------------------------------#
    def get_client_linklocal_ipv6(self):
        hostname = socket.gethostname()
        ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
        link_local = ipv6_list[0][4][0]
        if '%' in link_local:
            link_local = link_local.split('%')[0]
        return link_local

    # -----------------------------------GET Interface ID--------------------------------------#
    def client_interface_id(self):
        hostname = socket.gethostname()
        ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
        link_local = ipv6_list[0][4][0]
        if '%' in link_local:
            interface_id = link_local.split('%')[1]
        return interface_id

    # -----------------------------------GET Stateful IPv6 address--------------------------------------#
    def get_client_stateful_ipv6(self):
        # Check before using it
        hostname = socket.gethostname()
        ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
        Stateful = ipv6_list
        return Stateful

    # -----------------------------------GET Stateless IPv6 address--------------------------------------#
    def get_client_stateless_ipv6(self):
        # Check before using it
        hostname = socket.gethostname()
        ipv6_list = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
        Stateless = ipv6_list[0][8][0]
        return Stateless

    #   =================== String Byte conversion ================================================== #

    def string_convert_bytes(self, data):
        """
        Converting string value into bytes

        Arguments: The keyword takes 2 arguments.
        | Argument 1   |
        | data         |

        """
        try:
            byte_list = []
            binary_value = binascii.hexlify(data)
            byte_list.append(bytes(bytearray.fromhex(binary_value)))
            return byte_list
        except:
            raise AssertionError('Unable to perform string to byte convertion')

     #   ====================== File Byte conversion ================================================== #

    def read_file(self, sfile):
        """
        reading a file in binary format

        Arguments: The keyword takes 2 arguments.
        | Argument 1   |
        | sfile        |

        """
        try:
            with open(sfile, 'rb') as file_open:
                file_data = file_open.read()
            return file_data
        except:
            raise AssertionError('Unable to read file')

    def get_mac_address(self):
        """
        Retrives Client mac address

        """
        try:
            mac = hex(get_mac())[2:-1]
            return mac
        except Exception, msg:
            raise AssertionError('Error while retrieving mac address for router advertisement packet: ', msg)
