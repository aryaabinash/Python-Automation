from Packages.Interfaces.EWS.EWSKeywords import *
from Packages.Interfaces.SNMP.SNMPKeywords import *


class SNMPValidation:
    def __init__(self, printer_ip, product_family, product_name):
        self.printer_ip = printer_ip
        self.product_family = product_family
        self.product_name = product_name
        # Assigning path to 3 folders back from current folder
        self.path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
        self.config_file_dir = os.path.join(self.path, "Data", "SNMP_Config", self.product_family, self.product_name)
        self.sitemap = os.path.join(self.path, "Data", "EWS_Sitemaps", self.product_family, self.product_name, "Sitemap.xml")
        self.credential_file = os.path.join(self.path, "Data", "SNMP_Config", "Credentials.xml")
        self.snmp_obj = SNMPKeywords()
        self.snmp_obj.snmp_initialize(self.printer_ip)
    
    def validate_snmp_get(self, category, version, credentials_file='False'):
        """ This keyword is used to validate SNMP get operation .

        Arguments: The keyword takes 4 arguments.
        | Argument 1 | Argument 2  |       Argument 3       |
        |  Category  |  Version    |   credential_file(T/F) |
        """
        # Getting the respective Config file based on the Category mentioned in Test
        config_file = os.path.join(self.config_file_dir, 'Snmp_' + category) + '.xml'
        test_status = True

        if not os.path.exists(config_file):
            raise AssertionError("SNMP Config file for %s is not found in %s" % (category, self.config_file_dir))

        if credentials_file == 'True':
            credential_file_path = self.credential_file
        else:
            credential_file_path = None

        self.__version_configuration(version, credential_file_path)
        tree = ET.parse(config_file)
        root = tree.getroot()
        # For each OID in the Config File SNMP GET operation will be done
        for oid in root.getiterator('OID'):
            if version in oid.attrib['version']:
                try:
                    self.snmp_obj.snmp_get_operation(oid.attrib['value'], oid.attrib['type'])
                except Exception, msg:
                    test_status = False
                    print msg

        if test_status is False:
            raise AssertionError("Test Failed due to failure of few GET operations")

    def validate_snmp_root_walk(self, version, oid, credentials_file='False'):

        """ This keyword is used to validate SNMP Root walk operation .

       Arguments: The keyword takes 4 arguments.
       | Argument 1 | Argument 2  | |Argument 3 |  |Argument 4|
       |  Version  |  OID  |    |  None    |  |True/False |
       """
        if credentials_file == 'True':
            credential_file_path = self.credential_file
        else:
            credential_file_path = None
        self.__version_configuration(version, credential_file_path)

        try:
            self.snmp_obj.snmp_root_walk(oid)
        except Exception, msg:
            raise AssertionError(msg)

    def validate_snmp_get_next(self, category, version, credentials_file='False'):

        """ This keyword is used to validate SNMP get next operation .

               Arguments: The keyword takes 4 arguments.
               | Argument 1 | Argument 2  | |Argument 3 |  |Argument 4|
               |  Category  |  Version  |    |  None    |  |True/False |
        """
        config_file = os.path.join(self.config_file_dir, 'Snmp_' + category) + '.xml'
        test_status = True

        if not os.path.exists(config_file):
            raise AssertionError("SNMP Config file for %s is not found in %s" % (category, self.config_file_dir))

        if credentials_file == 'True':
            credential_file_path = self.credential_file
        else:
            credential_file_path = None
        self.__version_configuration(version, credential_file_path)

        tree = ET.parse(config_file)
        root = tree.getroot()
        # For those OIDs which has NEXT OID tag in Config, the GETNEXT operation will be performed
        for oid in root.getiterator('OID'):
            if version in oid.attrib['version']:
                for next_oid in oid.getiterator('NextOID'):
                    try:
                        self.snmp_obj.snmp_get_next_operation(oid.attrib['value'], oid.attrib['type'], next_oid.attrib['value'], next_oid.attrib['type'])
                    except Exception, msg:
                        test_status = False
                        print msg

        if test_status is False:
            raise AssertionError("Test Failed due to failure of few GETNEXT operations")

    def validate_snmp_walk(self, category, version, credentials_file='False'):

        """ This keyword is used to validate SNMP walk operation .

           Arguments: The keyword takes 4 arguments.
           | Argument 1 | Argument 2  | |Argument 3 |  |Argument 4|
           |  Category  |  Version  |    |  None    |  |True/False |
        """
        config_file = os.path.join(self.config_file_dir, 'Snmp_' + category) + '.xml'
        test_status = True

        if not os.path.exists(config_file):
            raise AssertionError("SNMP Config file for %s is not found in %s" % (category, self.config_file_dir))

        if credentials_file == 'True':
            credential_file_path = self.credential_file
        else:
            credential_file_path = None
        self.__version_configuration(version, credential_file_path)

        tree = ET.parse(config_file)
        root = tree.getroot()
        for oid in root.getiterator('OID'):
            if version in oid.attrib['version']:
                try:
                    self.snmp_obj.snmp_walk_operation(oid.attrib['value'], oid.attrib['type'])
                except Exception, msg:
                    test_status = False
                    print msg

        if test_status is False:
            raise AssertionError("Test Failed due to failure of few WALK operations")

    def validate_snmp_set(self, category, version, credentials_file='False'):

        """ This keyword is used to validate SNMP set operation .

           Arguments: The keyword takes 4 arguments.
           | Argument 1 | Argument 2  | |Argument 3 |  |Argument 4|
           |  Category  |  Version  |    |  None    |  |True/False |
        """
        config_file = os.path.join(self.config_file_dir, 'Snmp_' + category) + '.xml'
        test_status = True

        if not os.path.exists(config_file):
            raise AssertionError("SNMP Config file for %s is not found in %s" % (category, self.config_file_dir))

        if credentials_file == 'True':
            credential_file_path = self.credential_file
        else:
            credential_file_path = None
        self.__version_configuration(version, credential_file_path)

        tree = ET.parse(config_file)
        root = tree.getroot()
        # For those OIDs which has ValidValues and InValidVAlues tag, set operation will be performed on that OID with those values
        for oid in root.getiterator('OID'):
            if version in oid.attrib['version']:
                for valid_values in oid.getiterator('ValidValues'):
                    for indx in range(len(valid_values)):
                        try:
                            self.snmp_obj.snmp_set_value(oid.attrib['value'], oid.attrib['type'], valid_values[indx].text)
                        except Exception, msg:
                            test_status = False
                            print msg

                for invalid_values in oid.getiterator('InValidValues'):
                    for indx in range(len(invalid_values)):
                        try:
                            self.snmp_obj.snmp_set_invalid_value(oid.attrib['value'], oid.attrib['type'], invalid_values[indx].text)
                        except Exception, msg:
                            test_status = False
                            print msg

        if test_status is False:
            raise AssertionError("Test Failed due to failure of few SET operations")

    def snmp_v1v2_teardown(self):
        """ This keyword is used for v1v2 tear down while using the private community
        """

        try:
            adaptor = EWSKeywords()
            adaptor.ews_initialize(self.printer_ip, self.sitemap, 'firefox', self.path)

            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page("SNMP", "https")
            adaptor.ews_clear_text('Set_Community_Name')
            adaptor.ews_clear_text('Confirm_Set_Community_Name')
            adaptor.ews_clear_text('Get_Community_Name')
            adaptor.ews_clear_text('Confirm_Get_Community_Name')
            adaptor.ews_uncheck_checkbox('Disable_v1v2_default_Get_Community_Name_Public')
            adaptor.ews_click_button('Apply')
            time.sleep(5)
            adaptor.ews_click_button('OK')
            adaptor.ews_close_browser()

        except Exception, msg:
            raise AssertionError(msg)

    def snmp_v3_ews_setup(self):
        # This method is used to set the credentials file for SNMP V3 settings.

        print ('-' * 15) + ' Configure v3 setting through EWS ' + ('-' * 15)

        try:
            adaptor = EWSKeywords()
            adaptor.ews_initialize(self.printer_ip, self.sitemap, 'firefox', self.path)

            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page("Settings", "https")
            adaptor.ews_set_text('Password', 'admin')
            adaptor.ews_set_text('Confirm_password', 'admin')
            adaptor.ews_click_button('Apply')
            adaptor.ews_close_browser()

            tree = ET.parse(self.credential_file)
            root = tree.getroot()
            for version in root.getiterator('version'):
                if version.attrib['num'] == 'v3':
                    v3_username = version[0].text
                    v3_auth_protocol = version[1].text
                    v3_auth_password = version[2].text
                    v3_priv_protocol = version[3].text
                    v3_priv_password = version[4].text

            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page_with_credentials("SNMP", "https", "admin", "admin")

            adaptor.ews_click_button('Enable_v3')
            adaptor.ews_set_text('v3_username', v3_username)
            adaptor.ews_dropdown_select_by_text('v3_authentication_protocol', v3_auth_protocol)
            adaptor.ews_set_text('v3_authentication_key', v3_auth_password)
            adaptor.ews_dropdown_select_by_text('v3_privacy_protocol', v3_priv_protocol)
            adaptor.ews_set_text('v3_privacy_key', v3_priv_password)
            adaptor.ews_click_button('Apply')
            time.sleep(5)
            adaptor.ews_click_button('OK')
            adaptor.ews_close_browser()

        except Exception, msg:
            raise AssertionError(msg)

        print ('-' * 15) + ' Successfully Configured v3 settings ' + ('-' * 15)

    def snmp_v3_teardown(self):

        """ This keyword is used for v3 tear down
        """

        try:
            adaptor = EWSKeywords()
            adaptor.ews_initialize(self.printer_ip, self.sitemap, 'firefox', self.path)
            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page_with_credentials("SNMP", "https", "admin", "admin")
            adaptor.ews_click_button('Disable SNMPV3')
            adaptor.ews_click_button('Apply')
            time.sleep(5)
            adaptor.ews_click_button('OK')
            adaptor.ews_close_browser()

            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page_with_credentials("Settings", "https", "admin", "admin")
            adaptor.ews_clear_text('Password')
            adaptor.ews_clear_text('Confirm_password')
            adaptor.ews_click_button('Apply')
            time.sleep(5)
            adaptor.ews_click_button('OK')
            adaptor.ews_close_browser()

        except Exception, msg:
            raise AssertionError(msg)

    ##################### Private Methods ################

    def __version_configuration(self, version, credentials_file):

        # This method is used for version configuration.
        if version in ['1', '2']:
            # For setting version variable of SNMPKeywords
            if credentials_file:
                self.__ews_set_v1v2_settings(credentials_file)
            self.snmp_obj.snmp_set_v1v2_settings(version, credentials_file)

        elif version == '3':
            self.snmp_obj.snmp_set_v3_settings(credentials_file)

        else:
            raise AssertionError("Error : Unsupported SNMP version")

    def __ews_set_v1v2_settings(self, credentials_file):

        # This method is used for setting read and write mode from EWS page.

        print(('-' * 15) + ' Configure v1v2 setting through EWS ' + ('-' * 15))

        try:
            adaptor = EWSKeywords()
            adaptor.ews_initialize(self.printer_ip, self.sitemap, 'firefox', self.path)
            tree = ET.parse(credentials_file)
            root = tree.getroot()
            for version in root.getiterator('version'):
                if version.attrib['num'] == 'v1v2':
                    get_community_name = version[0].text
                    set_community_name = version[1].text

            adaptor.ews_open_browser()
            adaptor.ews_navigate_to_page("SNMP", "https")
            adaptor.ews_set_text('Set_Community_Name', set_community_name)
            adaptor.ews_set_text('Confirm_Set_Community_Name', set_community_name)
            adaptor.ews_set_text('Get_Community_Name', get_community_name)
            adaptor.ews_set_text('Confirm_Get_Community_Name', get_community_name)
            adaptor.ews_check_checkbox('Disable_v1v2_default_Get_Community_Name_Public')
            adaptor.ews_click_button('Apply')
            time.sleep(5)
            adaptor.ews_click_button('OK')
            adaptor.ews_close_browser()

        except Exception, msg:
            raise AssertionError(msg)

        print ('-' * 15) + ' Successfully Configured v1v2 settings ' + ('-' * 15)
