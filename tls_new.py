from NetworkLibrary.BaseOperations.BaseWiresharkOperation import BaseWiresharkOperation
from NetworkLibrary.BaseOperations.BaseTLSOperation import BaseTLSOperation
from HPWebLibrary.BaseOperations.BaseWebOperations import BaseWebOperations
from SnmpLibrary.BaseOperations.BaseSnmpOperations import BaseSnmpOperations
from HPWebLibrary.BaseOperations.BaseSettingsWebOperations import BaseSettingsWebOperations
import os
import time

class tls_new(BaseWiresharkOperation,BaseTLSOperation,BaseWebOperations,BaseSnmpOperations,BaseSettingsWebOperations):

    def tls_initialize(self, root_folder, printer_ip):
        self.cap = ''
        self.root_path = root_folder
        self.ws_capture_path = os.path.join(self.root_path, "Logs", "Wireshark_Captures", "TLS")
        if not os.path.exists(self.ws_capture_path):
            os.makedirs(self.ws_capture_path)

        self.printerip = printer_ip

    def start_tls_packet_capture(self, filename, interface='br0'):
        self.cap_filename = 'Testcase_' + filename
        ws_filter = 'host '+ str(self.printerip)

        try:
            self.start_wireshark_capture(file_name=(os.path.join(self.ws_capture_path, self.cap_filename)), interface=interface, ws_filter=ws_filter)
        except Exception, msg:
            raise AssertionError("Failed to Capture Packets -> %s" % str(msg))

    def stop_tls_packet_capture(self):
        try:
            self.stop_wireshark_capture(self.ws_capture_path)
            self.convert_cap_to_txt_file()

        except Exception, msg:
            raise AssertionError("Error in stopping wireshark capture -> %s" % str(msg))

    def validate_captured_packet(self, message, flag='True'):
        try:
            print 'Started Packet validation in ' + self.cap_filename + '.txt'
            filepath = os.path.join(self.ws_capture_path, self.cap_filename) + '.txt'
            print 'Keyword Searching is -> %s :: Should Found -> %s' % (message, flag)
            content = open(filepath, 'r').read()
            content= content.decode('utf8','ignore')
            if flag == 'True':
                if message in content:
                    print message + ' message found in the Packet - Expected Result'
                else:
                    raise AssertionError("%s Message not found in the Packet which is not expected" % message)
            else:
                if message not in content:
                    print message + ' message not found in the Packet - Expected Result'
                else:
                    raise AssertionError("%s Message found in the Packet which is not expected" % message)

        except Exception, msg:
            raise AssertionError("Unable to validate the expected packet -> %s" % str(msg))

    def tls_select_cipher_and_protocol_version(self, key):
        try:
            self.web_open_browser()
            self.web_navigate_to_page("Management Protocol")
            for value in range(len(key)):
                self.web_check_checkbox(key[value])
            self.web_click_button('Apply')
            time.sleep(20)
            self.web_click_button('OK')
            self.web_close_browser()
        except Exception as msg:
            raise AssertionError("Unable to check the checkbox - Error : %s" % msg)


    def tls_unselect_cipher_and_protocol_version(self, key):
        try:
            self.web_open_browser()
            self.web_navigate_to_page("Management Protocol")
            for value in range(len(key)):
                self.web_uncheck_checkbox(key[value])
            self.web_click_button('Apply')
            time.sleep(20)
            self.web_click_button('OK')
            self.web_close_browser()
        except Exception as msg:
            raise AssertionError("Unable to uncheck the checkbox - Error : %s" % msg)

    def tls_validate_checkbox_status(self,key):
        try:
            self.web_open_browser()
            self.web_navigate_to_page("Management Protocol")
            time.sleep(5)
            status = self.web_checkbox_ischecked(key)
            if status == True:
                print "Check box is enabled"
            else:
                raise AssertionError("check box is not enabled")
        except Exception as msg:
            raise AssertionError("Unable to validate checkbox status - Error : %s" % msg)

    def validate_https_success_status(self):
        try:
            self.web_open_browser()
            self.web_navigate_to_page("Management Protocol")
            time.sleep(5)
            self.web_close_browser()
        except Exception as msg:
            raise AssertionError("Unable to open the browser by using https - Error : %s" % msg)


    def validate_https_error_status(self,key):
        try:
            self.web_open_browser()
            self.web_navigate_to_page("Management Protocol")
            for value in range(len(key)):
                self.web_uncheck_checkbox(key[value])
            self.web_click_button('Apply')
            time.sleep(4)
            self.web_click_button("Alert_ok")
        except Exception as msg:
            raise AssertionError("Error message did not come, which is not expected - Error : %s" % msg)

    def tls_snmp_set_operation(self,oid_key, set_value,oid_type=None):
        try:
            if 'x' in set_value:
                self.snmp_set_value_operation(oid_key,set_value,oid_type = 'string')
            else:
                self.snmp_set_value_operation(oid_key, int(set_value))
        except Exception as msg:
            raise AssertionError("Unable to do set operation - Error : %s" %msg)

    def validate_snmp_get_operation(self,oid_key,tls_version):
        try:
            values=self.snmp_get_value_operation(oid_key)
            if values not in [tls_version]:
                raise AssertionError("Error ->TLS version is not present")
        except Exception as msg:
            raise AssertionError("Expected value did not come - Error : %s" %msg)

    def validate_snmp_walk_oids(self,oid_key,walk_oid):
        try:
            received_oid = self.snmp_get_value_operation(oid_key)
            walk_oid = ','.join(walk_oid)
            received_oid = received_oid.strip(' " ')
            print "Received oids are", received_oid
            print "Given oids are", walk_oid
            if walk_oid == received_oid:
                print "Walk operation validated successfully"
            else:
                raise AssertionError("Walk operation did not match as expected")

        except Exception as msg:
            raise AssertionError("Unable to do validate walk operations - Error : %s" %msg)






