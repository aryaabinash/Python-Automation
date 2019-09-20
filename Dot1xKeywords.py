import requests
import shutil
from lxml import etree
import datetime
import os

from Packages.Utilities.Wireshark import *
from Packages.Utilities.SwitchKeywords import *
from Packages.Wrappers.EWSWrapper import *
from Packages.Wrappers.SNMPWrapper import *


class Dot1xKeywords:
    def __init__(self, product_family, product_name, printer_ip, switch_ip, auth_port, browser, root_folder, username, password , Signinelement):
        self.product_family = product_family
        self.product_name = product_name
        self.printer_ip = printer_ip
        self.switch_ip = switch_ip
        self.auth_port = auth_port
        self.browser = browser
        self.cap_filename = ''

        self.radius_ip = ''
        self.radius_username = ''
        self.radius_password = ''

        self.username = username
        self.password = password
        self.Signinelement = Signinelement

        # Getting the root_folder
        self.root_path = root_folder

        # Getting the file path for capturing Wireshark Logs
        self.ws_capture_path = os.path.join(self.root_path, "Logs", "Wireshark_Captures", "802_1x")

        # Getting the file path for Sitemap based on the product family and product name
        self.sitemap = os.path.join(self.root_path, "Data", "EWS_Sitemaps", self.product_family, self.product_name, "Sitemap.xml")

        # Getting the dot1x config file's filepath
        self.dot1x_config_file = os.path.join(self.root_path, "Data", "802_1x", "Default_dot1x_Settings.xml")
        self.dot1x_restore_file = os.path.join(self.root_path, "Data", "802_1x", "Restore_dot1x_Settings.xml")
        self.psexec = os.path.join(self.root_path, "Applications", "PsExec.exe")

        # Path for SelfSigned certificate's xml
        self.self_sign_cert_path = os.path.join(self.root_path,  "Data", "802_1x", "Certificates", "Valid", "SelfSigned.xml")

        # Path for valid Certificates
        self.valid_ca_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Valid", "CACert.xml")
        self.valid_id_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Valid", "ID_cert.pfx")
        self.valid_password = 'xyzzy'

        # Path for Invalid Certificates
        self.invalid_ca_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Invalid", "CACert_Invalid.xml")
        self.invalid_id_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Invalid", "SPIJetdirectCert.pfx")
        self.invalid_password = 'JetDirect'

        # Path for Expired Certificates
        self.expired_ca_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Expired", "CACert_Expired.xml")
        self.expired_id_cert_path = os.path.join(self.root_path, "Data", "802_1x", "Certificates", "Expired", "client-cert.pfx")
        self.expired_password = 'Q1w2e3r4'

        self.dot1x_params = {}
        self.xml_to_put = ''

        # Creating objects for Utility packages ,Wireshark and SwitchKeywords
        self.ws_capture = Wireshark()
        self.switch_handler = SwitchKeywords(self.switch_ip)
        self.ews_handler = EWSWrapper(self.printer_ip, self.sitemap, self.browser, self.root_path, self.username, self.password, self.Signinelement)

        # Creating Log folder if it doesn't exist
        if not os.path.exists(self.ws_capture_path):
            os.makedirs(self.ws_capture_path)

        # Initialize the dot1x parameters with the default value mentioned in 'Default_dot1x_Settings.xml'
        self.__dot1x_default_settings()

    def configure_dot1x_settings(self, **kwparams):
        """
        This method will do the following actions
         1) will take the keywords arguments and re assign the dot1x parameters if there any.
         2) make a copy of 'Restore_dot1x_Settings.xml' as 'dot1x_config.xml'
         3) Update the 'dot1x_config.xml' with the values in the dictionary - dot1x_params
         4) Do a PUT operation
         4) Will remove the file 'dot1x_config.xml' which is created at run time

        Arguments: The keyword takes 1 argument.
        | Argument 1 |
        | kwparams   |

        """

        print 'Configuring Dot1x parameters'

        root_xpath = '/io:Profile/io:AdapterProfile/io:EthProfile/io:WiredEnterprise/'
        namespace = {'io': 'http://www.hp.com/schemas/imaging/con/ledm/iomgmt/2008/11/30', 'dd': 'http://www.hp.com/schemas/imaging/con/dictionaries/1.0/'}

        # Copy 'Restore_dot1x_Settings.xml' and save as 'dot1x_config.xml'
        try:
            shutil.copy(self.dot1x_restore_file, "dot1x_config.xml")

        except IOError, msg:
            raise AssertionError("Unable to copy the 'Restore_dot1x_Settings.xml' -> %s" % str(msg))

        try:
            tree = etree.parse("dot1x_config.xml")

        except ParseError:
            raise AssertionError("Error in Parsing the 'dot1x_config.xml' file")

        # Using keyword Arguments, updating the dot1x parameters
        for key in kwparams.keys():
            self.dot1x_params[key] = str(kwparams[key])

        try:
            print '-' * 20
            print 'Protocol -> '+str(self.dot1x_params['protocol'])

            if self.dot1x_params['protocol'].lower() == 'none':
                pass
            else:
                if self.dot1x_params['protocol'] == 'PEAP':
                    protocol_xpath = root_xpath + 'dd:Protocols802.1x/dd:PEAP'
                elif self.dot1x_params['protocol'] == 'EAP-TLS':
                    protocol_xpath = root_xpath + 'dd:Protocols802.1x/dd:EAP_TLS'
                else:
                    raise AssertionError("Unsupported Protocol type")

                address = tree.xpath(protocol_xpath, namespaces=namespace)
                address[0].text = 'enabled'

            print 'Username -> '+str(self.dot1x_params['username'])
            username_xpath = root_xpath + 'dd:UserName'
            address = tree.xpath(username_xpath, namespaces=namespace)
            address[0].text = self.dot1x_params['username']

            print 'Password -> ' + str(self.dot1x_params['password'])
            password_xpath = root_xpath + 'dd:Password'
            address = tree.xpath(password_xpath, namespaces=namespace)
            address[0].text = self.dot1x_params['password']

            if self.dot1x_params['server_id']:
                print 'Server ID -> ' + str(self.dot1x_params['server_id'])
                serverid_xpath = root_xpath + 'dd:ServerID'
                address = tree.xpath(serverid_xpath, namespaces=namespace)
                address[0].text = self.dot1x_params['server_id']

            print 'Encryption Strength -> ' + str(self.dot1x_params['encryption_strength'])
            encryption_xpath = root_xpath + 'dd:EncryptionStrength'
            address = tree.xpath(encryption_xpath, namespaces=namespace)
            address[0].text = self.dot1x_params['encryption_strength']

            servermatch_xpath = root_xpath + 'dd:RequireExactServerMatch'
            address = tree.xpath(servermatch_xpath, namespaces=namespace)
            address[0].text = self.dot1x_params['require_server_match']

            authfailure_xpath = root_xpath + 'dd:AuthFailureAction'
            address = tree.xpath(authfailure_xpath, namespaces=namespace)
            address[0].text = self.dot1x_params['auth_failure_action']

            tree.write("dot1x_config.xml", encoding='utf-8', xml_declaration=True)
            print '-' * 20
            print 'Successfully Updated the XML for Dot1x Configuration'

        except Exception, msg:
            raise AssertionError("Error in Updating values in xml - dot1x_config.xml -> %s" % str(msg))

        self.xml_to_put = "dot1x_config.xml"

        try:
            self.__perform_put_operation()
            print 'Successfully configured the dot1x settings in Printer'

        except Exception, msg:
            raise AssertionError("Failed to Update Dot1x Config values -> %s" % str(msg))

        # Removing the file which created during runtime
        if os.path.exists("dot1x_config.xml"):
            os.remove("dot1x_config.xml")

    def start_dot1x_packet_capture(self, filename):
        """
        Will invoke the wireshark capture method which will capture the Dot1x packets and save in pcap format
        Arguments: The keyword takes 1 argument.
        | Argument 1 |
        | Filename   |
        """
        self.cap_filename = 'Testcase_' + filename
        try:
            self.ws_capture.start_wireshark_capture(os.path.join(self.ws_capture_path, self.cap_filename), '-f "ether proto 0x888e" ')

        except Exception, msg:
            raise AssertionError("Failed to Capture Packets -> %s" % str(msg))

    def stop_dot1x_packet_capture(self):
        """
        Will Stop the wireshark capture and make a copy of pcap file in txt format

        """
        try:
            self.ws_capture.stop_wireshark_capture(self.ws_capture_path)
            self.ws_capture.convert_cap_to_txt_file()

        except Exception, msg:
            raise AssertionError("Error in stopping wireshark capture -> %s" % str(msg))

    def enable_authenticated_port(self):
        """
        Method will enable the port as Authenticated Port
        """
        try:
            self.switch_handler.enable_port_as_authenticated(self.auth_port)
            time.sleep(20)

        except Exception, msg:
            raise AssertionError(str(msg))

    def disable_authenticated_port(self):
        """
        Method will enable the port as Non Authenticated Port
        """
        try:
            self.switch_handler.enable_port_as_non_authenticated(self.auth_port)
            time.sleep(20)

        except Exception, msg:
            raise AssertionError(str(msg))

    def hose_break(self):
        """
        Method will disable the Port in the switch
        """
        try:
            self.switch_handler.disable_port(self.auth_port)
            time.sleep(10)

        except Exception, msg:
            raise AssertionError(str(msg))

    def hose_connect(self):
        """
        Method will enable the Port in the switch
        """
        try:
            self.switch_handler.enable_port(self.auth_port)
            time.sleep(10)

        except Exception, msg:
            raise AssertionError(str(msg))

    def validate_captured_packet(self, message, flag='True'):
        """
        Method will do the following validation
        a) Will Search for the value specified in 'message' variable in the Captured txt file
        b) flag field is to mention whether the value specified in 'message' variable is expected in the file or not
           and will pass/fail depends on the result
        Arguments: The keyword takes 2 arguments.
        | Argument 1 |  Argument 2 |
        | Message    |  Flag       |
        """
        print 'Started Packet validation in ' + self.cap_filename + '.txt'
        filepath = os.path.join(self.ws_capture_path, self.cap_filename) + '.txt'
        print 'Keyword Searching is -> %s :: Should Found -> %s' % (message, flag)

        if flag == 'True':
            if message in open(filepath).read():
                print message + ' message found in the Packet - Expected Result'
            else:
                raise AssertionError("%s Message not found in the Packet which is not expected" % message)

        else:
            if message not in open(filepath).read():
                print message + ' message not found in the Packet - Expected Result'
            else:
                raise AssertionError("%s Message found in the Packet which is not expected" % message)

    def restore_dot1x_settings(self):
        """
        Will reset the Dot1x settings
        """
        print 'Resetting Dot1x Configuration..'
        self.xml_to_put = self.dot1x_restore_file

        try:
            self.__perform_put_operation()
            print 'Resetting Dot1x Configuration completed'

        except Exception, msg:
            raise AssertionError("Failed to reset Dot1x Configuration -> %s" % str(msg))

    def delete_temp_files(self):
        """
        Method to remove temperory files which created during run time
        """
        print 'Removing files which created during runtime'

        # Removing the Captured text file which created during runtime

        files = os.listdir(self.ws_capture_path)
        files_to_delete = [f for f in files if f.endswith('.txt')]
        print files_to_delete

        for _file in files_to_delete:
            os.remove(os.path.join(self.ws_capture_path, _file))

    def is_certificates_installed(self):
        """
        Method will check whether any CA certificate is installed
        """

        print 'Checking whether Certificates are installed'

        try:
            response = requests.get("https://" + self.printer_ip + "/Security/CACertificate", verify=False)
            if response.status_code == 200:
                print 'Certificates are already installed'
                return True
            elif response.status_code == 204:
                print 'Certificates are not installed'
                return False
            else:
                raise AssertionError("Unable to fetch the certificate installation status ")

        except Exception, msg:
            raise AssertionError(msg)

    def install_ca_certificate(self, cert_type='Valid'):
        """
        Method will Install the CA certificate based on the type
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Cert Type    |
        """
        print 'Installing %s CA certificate using LEDM' % cert_type
        if cert_type == 'Valid':
            cert_path = self.valid_ca_cert_path

        elif cert_type == 'Invalid':
            cert_path = self.invalid_ca_cert_path

        elif cert_type == 'Expired':
            cert_path = self.expired_ca_cert_path

        else:
            raise AssertionError("Certificate type in not Valid")

        try:
            content = open(cert_path, "r")
            payload = content.read()
            header = {'Content-Type': 'text/xml'}
            response = requests.post("https://" + self.printer_ip + "/Security/CACertificate", data=payload, headers=header,
                                     verify=False)

            if response.status_code == 201:
                print 'Successfully installed %s CA certificate' % cert_type

            else:
                raise AssertionError("Failed to Install the certificate using LEDM")

        except Exception, msg:
            raise AssertionError(msg)

    def install_id_certificate(self, cert_type='Valid'):
        """
        Method will Install the ID certificate based on the type
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Cert Type    |
        """
        if cert_type == 'Valid':
            cert_path = self.valid_id_cert_path
            password = self.valid_password

        elif cert_type == 'Invalid':
            cert_path = self.invalid_id_cert_path
            password = self.invalid_password

        elif cert_type == 'Expired':
            cert_path = self.expired_id_cert_path
            password = self.expired_password

        else:
            raise AssertionError("Certificate type in not Valid")

        try:
            self.ews_handler.ews_install_id_certificate(cert_path, password)

        except Exception, msg:
            raise AssertionError(msg)

    def delete_ca_certificate(self):
        """
        Method will delete all the installed CA certificates
        """
        print 'Deleting all installed CA certificates'

        try:
            # Getting info of all installed CA certificates
            data = requests.get("https://" + self.printer_ip + "/Security/CACertificate", verify=False)
            if data.status_code != 200:
                raise AssertionError("Failed to fetch the details of installed CA certificates")

            file_writer = open("cert1.xml", 'w')
            file_writer.write(data.content)
            file_writer.close()

            xpath = '/cert:CACertificateList/cert:CertificateData/cert:ResourceURL'
            tree = etree.parse("cert1.xml")
            address = tree.xpath(xpath, namespaces={'cert': 'http://www.hp.com/schemas/imaging/con/certificates/2011/01/19'})

            # Deleting all installed CA Certificates
            for cert_id in range(len(address)):
                print address[cert_id].text
                delete_uri = address[cert_id].text
                data = requests.delete("https://" + self.printer_ip + delete_uri, verify=False)
                if data.status_code != 200:
                    raise AssertionError("Failed to delete CA certificate - Response of delete is %s" % str(data.status_code))

            print 'Successfully deleted all CA certificates'

            # Removing the file which created during runtime
            if os.path.exists("cert1.xml"):
                os.remove("cert1.xml")

        except Exception, msg:
            raise AssertionError(msg)

    def delete_id_certificate(self):
        """
        Method will install the self-signed certificate
        """
        print 'Deleting Printer certificate (Installing Self Signed Certificate) using LEDM'

        try:
            content = open(self.self_sign_cert_path, "r")
            payload = content.read()
            header = {'Content-Type': 'text/xml'}
            response = requests.post("https://" + self.printer_ip + "/Security/DeviceCertificates/SelfSigned", data=payload, headers=header,
                                 verify=False)

            if response.status_code == 201:
                print 'Successfully installed self signed certificate'

            else:
                raise AssertionError("Failed to Install self-signed the certificate using LEDM")

        except Exception, msg:
            raise AssertionError(msg)

    def change_radius_server_date(self, years):
        """
        Method will add the years mentioned in 'Years' to the Radius server's timestamp
        """
        try:
            current_date = datetime.datetime.now()
            new_date = current_date.replace(year=current_date.year + int(years))
            f_new_date = new_date.strftime("%m-%d-%y")
            cmd = 'date ' + f_new_date

            final_cmd = self.psexec + ' -u ' + self.radius_username + ' -p ' + self.radius_password + ' \\\\' + self.radius_ip + ' -s -d cmd.exe /c ' + cmd
            os.system(final_cmd)

        except Exception, msg:
            raise AssertionError(msg)

    def set_authentication_priority_on_server(self, protocol):
        """
        Method will change the priority of authentication on Radius Server
        """
        try:
            if protocol == 'PEAP':
                profile_data = 'profiledata = "19000000000000000000000000000000" profiledata = "0D000000000000000000000000000000"'
            elif protocol == 'EAP-TLS':
                profile_data = 'profiledata = "0D000000000000000000000000000000" profiledata = "19000000000000000000000000000000"'
            else:
                raise AssertionError("Invalid Protocol type")
            cmd = 'netsh nps set np name = "policynew" state = "enable" processingorder = "1" policysource = "0" conditionid = "0x3d" conditiondata = "^15$|^19$|^17$|^18$" profileid = "0x100f" profiledata = "TRUE" profileid = "0x100a" ' + profile_data + ' profileid = "0x1009" profiledata = "0x5" profiledata = "0x3" profiledata = "0x9" profiledata = "0x4" profiledata = "0xa"'

            final_cmd = self.psexec + ' -u ' + self.radius_username + ' -p ' + self.radius_password + ' \\\\' + self.radius_ip + ' -s -d cmd.exe /c ' + cmd
            os.system(final_cmd)

        except Exception, msg:
            raise AssertionError(msg)

    def reset_radius_server_date(self):
        """
        Method will reset the Radius server's timestamp (Current timestamp)
        """
        try:
            current_date = datetime.datetime.now()
            f_new_date = current_date.strftime("%m-%d-%y")
            cmd = 'date ' + f_new_date

            final_cmd = self.psexec + ' -u ' + self.radius_username + ' -p ' + self.radius_password + ' \\\\' + self.radius_ip + ' -s -d cmd.exe /c ' + cmd
            os.system(final_cmd)

        except Exception, msg:
            raise AssertionError(msg)

    def reset_ipconfig_mode(self,manual_ip):
        """
        Method will change the IPconfig mode to DHCP
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Manual IP    |
        """
        try:
            snmp_handler = SNMPWrapper(manual_ip)
            snmp_handler.snmp_set_ipconfig_to_dhcp()

        except Exception, msg:
            raise AssertionError(msg)

    def change_printer_date_by_add_years(self,years):
        """
        Method will call EWS Wrapper function to change the date of the printer by adding years mentioned in parameter
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Years    |
        """
        try:
            self.ews_handler.ews_change_printer_date_by_add_years(years)
        except Exception, msg:
            raise AssertionError(msg)

    #***************** Private Method **********************

    def __dot1x_default_settings(self):
        # Parsing the 'Default_dot1x_Settings.xml' and initializing the dot1x parameters
        try:
            tree = ET.parse(self.dot1x_config_file)

        except ParseError:
            raise AssertionError("Error in Parsing the 'Default_dot1x_Settings.xml' file")

        root = tree.getroot()

        try:
            for params in root.getiterator('Default'):
                self.dot1x_params['protocol'] = params.find('protocol').text
                self.dot1x_params['username'] = params.find('username').text
                self.dot1x_params['password'] = params.find('password').text
                self.dot1x_params['server_id'] = params.find('server_id').text
                self.dot1x_params['encryption_strength'] = params.find('encryption_strength').text
                self.dot1x_params['require_server_match'] = params.find('require_server_match').text
                self.dot1x_params['auth_failure_action'] = params.find('auth_failure_action').text
                self.radius_ip = params.find('radius_ip').text
                self.radius_username = params.find('radius_username').text
                self.radius_password = params.find('radius_password').text
        except Exception, msg:
            raise AssertionError("Error in assigning dot1x default parameters -> %s" % str(msg))

    def __perform_put_operation(self):
        # Since the URI is constant for Dot1x operation, URI is hard-coded in the PUT command. The xml to be PUT will be saved in other method
        #  in the file mentioned in 'xml_to_put'
        try:
            content = open(self.xml_to_put, "r")
            payload = content.read()
            header = {'Content-Type':'text/xml'}
            response = requests.put("https://" + self.printer_ip + "/IoMgmt/Adapters/Eth0/Profiles/Active", data=payload, headers=header, verify=False, proxies={'http':'','https':''})

            if response.status_code == 200:
                print 'PUT operation Success ' + str(response.status_code)
            else:
                raise AssertionError("Response Code for PUT operation is %s" % (str(response.status_code)))

            time.sleep(30)
        except Exception, msg:
            raise AssertionError("PUT operation Failed -> %s" % str(msg))
