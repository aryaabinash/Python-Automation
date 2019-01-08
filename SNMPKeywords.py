import subprocess
import xml.etree.ElementTree as ET
import time

from robot.api import logger


class SNMPKeywords:

    def __init__(self):
        self.version = ''
        self.printer_ip = ''
        self.snmp_command = ''
        self.response = ''
        # If the credential file is not passed while version setting, by default community will be public
        self.get_community_name = 'public'
        self.set_community_name = 'public'
        self.v3_username = ''
        self.v3_auth_protocol = ''
        self.v3_auth_password = ''
        self.v3_priv_protocol = ''
        self.v3_priv_password = ''

    def snmp_initialize(self, printer_ip):
        self.printer_ip = printer_ip

    def snmp_set_v1v2_settings(self, version, credentials_file=None):
        if version == '2':
            # For version 2, in the command for SNMP operation, the version parameter value is 2c
            self.version = '2c'
        else:
            self.version = '1'
        # If credential file is passed, the community will be private and the values will be taken from credential file
        if credentials_file:
            tree = ET.parse(credentials_file)
            root = tree.getroot()
            for version in root.getiterator('version'):
                if version.attrib['num'] == 'v1v2':
                    self.get_community_name = version[0].text
                    self.set_community_name = version[1].text

    def snmp_set_v3_settings(self, credentials_file=None):

        self.version = '3'
        # Credentials for v3 settings will be taken from credential file and will raise assertion if not passed
        if credentials_file:
            tree = ET.parse(credentials_file)
            root = tree.getroot()
            for version in root.getiterator('version'):
                if version.attrib['num'] == 'v3':
                    self.v3_username = version[0].text
                    self.v3_auth_protocol = version[1].text
                    self.v3_auth_password = version[2].text
                    self.v3_priv_protocol = version[3].text
                    self.v3_priv_password = version[4].text

        else:
            raise AssertionError("Error : Please provide the credentials file")

    def snmp_get_operation(self, oid, type_):

        """ This keyword is used to do the get operation on the OIDs .
        
        Arguments: The keyword takes 2 arguments.
        | Argument 1 | Argument 2  |
        |     OID    |  data type  |
        """

        print ('-' * 15) + ' SNMP GET Operation ' + ('-' * 15)
        print 'OID : %s - Type : %s ' % (oid, type_)

        # Generating snmp GET command
        if self.version == '3':
            self.snmp_command = 'snmpget -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s ' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid)

        else:
            self.snmp_command = 'snmpget -v %s -c %s %s %s' % (self.version, self.get_community_name,
                                                                      self.printer_ip, oid)
        try:
            self.__execute_command()

            # If the Keywords mentioned below is not there in the response means the GET operation is failed
            if (type_.upper() not in self.response.upper() and ('SNMPv2-SMI' not in self.response) and ('iso' not in self.response)):
                raise AssertionError("Error -> SNMP Get Failed -> %s " % self.response)

            else:
                print 'Successfully performed SNMP Get Operation -> %s ' % self.response

        except Exception, msg:
            raise AssertionError('SNMP Get operation Failed : %s' % msg)

    def snmp_get_value(self, oid, type_):

        """ This keyword is used to get the value of the OID by doing get operation on that particular OIDs .

        Arguments: The keyword takes 2 arguments.
        | Argument 1 | Argument 2  |
        |     OID    |  data type  |
        """
        print ('-' * 15) + ' SNMP GET Value Operation ' + ('-' * 15)
        print 'OID : %s - Type : %s ' % (oid, type_)
        # Generating snmp GET command
        if self.version == '3':
            self.snmp_command = 'snmpget -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s ' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid)

        else:
            self.snmp_command = 'snmpget -v %s -c %s %s %s' % (self.version, self.get_community_name,
                                                                      self.printer_ip, oid)
        try:
            self.__execute_command()

            if (type_.upper() not in self.response.upper() and ('SNMPv2-SMI' not in self.response) and ('iso' not in self.response)):
                raise AssertionError("Error -> SNMP Get Failed -> %s " % self.response)

            else:
                print 'Successfully performed SNMP Get Operation -> %s ' % self.response
                # Extracting the value needed from the response
                response = [w.strip() for w in ((self.response.split('='))[1].strip()).split(':',1)]
                if len(response) > 1:
                    return_value = response[1]
                else:
                    return_value = ''
                print 'The value returned is %s' % return_value
                return return_value

        except Exception, msg:
            raise AssertionError('SNMP Get operation Failed : %s' % msg)
        
    def snmp_get_next_operation(self, oid, type_, next_oid, next_oid_type_):

        """ This keyword is used to get the next OID for the current OID by doing getnext operation.

        Arguments: The keyword takes 4 arguments.
        | Argument 1 | Argument 2  | |Argument 3 |  |Argument 4|
        |     OID    |  data type  | |  Next OID  | |Next OID data type |
        """

        print ('-' * 15) + ' SNMP GET NEXT Operation ' + ('-' * 15)
        print 'OID : %s - Next OID : %s - Type : %s ' % (oid, next_oid, type_)
        # Generating snmp GET NEXT command
        if self.version == '3':
            self.snmp_command = 'snmpgetnext -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s ' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid)

        else:
            self.snmp_command = 'snmpgetnext -v %s -c %s %s %s' % (self.version, self.get_community_name, self.printer_ip, oid)

        try:
            self.__execute_command()
            print 'SNMP GetNext on OID - %s -> %s' % (oid, self.response)
            get_next_response = self.response

            # Validating the GETNEXT operation by doing GET on NEXT OID. The response of GETNEXT and the response of GET on the NEXT OID should be same
            print 'Validating GetNext by doing SNMP GET on Next OID - %s' % next_oid
            self.snmp_get_operation(next_oid, next_oid_type_)
            get_response = self.response

            if get_next_response != get_response:
                raise AssertionError("Error -> Next Oid in Config File not matching with exact next oid ")

            else:
                print 'Both Responses are Matching'            
                print 'Successfully performed SNMP Get Next Operation'

        except Exception, msg:
            raise AssertionError('SNMP GetNext operation Failed -> %s' % msg)

    def snmp_walk_operation(self, oid, type_):

        """ This keyword is used to do snmp walk operation on individual OID  .

        Arguments: The keyword takes 2 arguments.
        | Argument 1 | Argument 2  |
        |     OID    |  data type  |
        """
        print ('-' * 15) + ' SNMP WALK Operation ' + ('-' * 15)
        print 'OID : %s - Type : %s ' % (oid, type_)

        # Generating snmp WALK command
        if self.version == '3':
            self.snmp_command = 'snmpwalk -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s ' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid)

        else:
            self.snmp_command = 'snmpwalk -v %s -c %s %s %s' % (self.version, self.get_community_name,
                                                                       self.printer_ip, oid)

        try:
            self.__execute_command()

            if (type_.upper() not in self.response.upper() and ('SNMPv2-SMI' not in self.response) and ('iso' not in self.response)):
                raise AssertionError("Error -> SNMP Walk Failed -> %s " % self.response)

            else:
                print 'Successfully performed SNMP Walk Operation -> %s ' % self.response

        except Exception, msg:
            raise AssertionError('SNMP Walk operation Failed -> %s' % msg)

    def snmp_root_walk(self, oid):

        """This keyword is used to do snmp root walk operation on root OID

        Arguments: The keyword takes 2 arguments.
            | Argument 1 | Argument 2  |
            |     OID    |  data type  |
        """

        print ('-' * 15) + ' SNMP WALK Operation on Root OId ' + ('-' * 15)

        # Generating snmp WALK command
        if self.version == '3':
            self.snmp_command = 'snmpwalk -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s ' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid)

        else:
            self.snmp_command = 'snmpwalk -v %s -c %s %s %s' % (self.version, self.get_community_name,
                                                                       self.printer_ip, oid)

        try:
            self.__execute_command()

            if 'No Response' in self.response:
                raise AssertionError("Error -> SNMP Walk Failed -> %s " % self.response)

            else:
                print 'Successfully performed SNMP Walk Operation -> %s ' % self.response

        except Exception, msg:
            raise AssertionError('SNMP Walk operation Failed -> %s' % msg)

    def snmp_set_value(self, oid, type_, set_value, validation=True):

        """ This keyword is used to set the valid value for supported OIDs .

        Arguments: The keyword takes 4 arguments.
        | Argument 1 | Argument 2  | | Argument 3 |     |Argument 4 |
        |     OID    |  data type  | | Value to be set | | True/False |
        """
        print ('-' * 15) + ' SNMP SET Operation ' + ('-' * 15)
        print 'OID : %s - Type : %s - ValueToSet : %s ' % (oid, type_, set_value)

        # The values used in command depends on the type
        if type_ == 'Integer':
            type_var = 'i'
        elif type_ == 'IpAddress':
            type_var = 'a'            
        else:
            type_var = 's'

        # Generating snmp SET command
        if self.version == '3':
            self.snmp_command = 'snmpset -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s %s %s' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid, type_var, set_value)

        else:
            self.snmp_command = 'snmpset -v %s -c %s %s %s %s %s' % (
                self.version, self.set_community_name, self.printer_ip, oid, type_var, set_value)

        try:
            self.__execute_command()

            time.sleep(5)

            # Validation 1 - Validating the response
            if (type_.upper() not in self.response.upper() and ('SNMPv2-SMI' not in self.response) and ('iso' not in self.response)):
                raise AssertionError("Error -> SNMP SET Failed -> %s " % self.response)
            else:
                print 'Successfully performed SNMP SET Operation -> %s ' % self.response

            if validation:
                # Validation 2 - Validating after doing GET on the same oid
                print 'Validating SNMP SET operation by performing GET on the same OID'
                self.snmp_get_operation(oid, type_)
                self.__snmp_validate_set_response(type_, set_value)

        except Exception, msg:
            raise AssertionError('SNMP Set operation Failed -> %s' % msg)

    def snmp_set_invalid_value(self, oid, type_, set_value):

        """ This keyword is used to set invalid value for suported OIDs .

        Arguments: The keyword takes 4 arguments.
        | Argument 1 | Argument 2  | | Argument 3 |     |Argument 4 |
        |     OID    |  data type  | | Value to be set | | True/False |
        """

        print ('-' * 15) + ' SNMP SET Operation(Invalid Value) ' + ('-' * 15)
        print 'OID : %s - Type : %s - ValueToSet : %s ' % (oid, type_, set_value)

        # The values used in command depends on the type
        if type_ == 'Integer':
            type_var = 'i'
        elif type_ == 'IpAddress':
            type_var = 'a'    
        else:
            type_var = 's'

        # Generating snmp SET command
        if self.version == '3':
            self.snmp_command = 'snmpset -v %s -u %s -l authPriv -n Jetdirect -a %s -A %s -x %s -X %s %s %s %s \'%s\'' % (
                self.version, self.v3_username, self.v3_auth_protocol, self.v3_auth_password,
                self.v3_priv_protocol, self.v3_priv_password, self.printer_ip, oid, type_var, set_value)

        else:
            self.snmp_command = 'snmpset -v %s -c %s %s %s %s \'%s\'' % (
                self.version, self.set_community_name, self.printer_ip, oid, type_var, set_value)

            self.__execute_command(True)
            
            # Validation 1 - Validating the response
            if ('Error in packet' not in self.response) and ('Bad value' not in self.response):
                raise AssertionError("Error: Not permitted values has been set")
            else:
                print 'Validation Success - Invalid values Not accepted'

            # Validation 2 - Validating after doing GET on the same oid
            print 'Validating SNMP SET operation by performing GET on the same OID'
            self.snmp_get_operation(oid, type_)
            # Since this is an inverse Validation, 3rd parameter should be True
            self.__snmp_validate_set_response(type_, set_value, True)

        ##################### Private Methods ##########################
    def __execute_command(self, return_error=False):

        # This method is used to execute the command.

        self.response = ''
        try:
            print self.snmp_command
            # self.response will have the response of command execution which will further used for Validation
            self.response = subprocess.check_output(self.snmp_command, stderr=subprocess.STDOUT, shell=True)
            time.sleep(5)

        except subprocess.CalledProcessError as err:
            if return_error:
                self.response = err.output
            else:
                raise AssertionError(err.output)

        except Exception, msg:
            raise AssertionError(msg)

    def __snmp_validate_set_response(self, type_, value, inverse_validation=False):

        # This method is used to validate the snmp set value.

        type_ = type_.upper()

        response = [(w.strip()).upper() for w in ((self.response.split('='))[1].strip()).split(':')]

        # For validating SNMP SET for Invalid Values
        if inverse_validation:
            if response == [type_, str(value).upper()]:
                raise AssertionError("SET Validation Failed(Invalid Values)")
            else:
                print 'SNMP SET validation(Invalid Values) successfully completed'

        # For validating SNMP SET for Valid Values
        else:
            if response != [type_, str(value).upper()]:
                raise AssertionError("SET Validation Failed")
            else:
                print 'SNMP SET validation successfully completed'
