import socket
import random
import json
import requests
import os
import subprocess

class ACL_Keywords():
    def __init__(self,printer_ip):
        self.printer_ip = printer_ip
        self.uri = 'http://'+self.printer_ip+'/cdm/acl/v1/configuration'
        self.json_data=''
        self.headers = {'Content-Type': 'application/json'}
        self.value=''
        self.default = {'httpBypassEnabled':'true','version':'1.0.0','aclEnabled':'false'}
        self.response = ''

    def default_acl_settings(self):
        """This method will do the default ACL settings on printer.
        In default settings acl option should be disabled and httpbypass should be enabled"""
        try:
            self.__acl_put_operation(self.default)
            self.validate_default_settings()
        except Exception, msg:
            raise  AssertionError(msg)

    def validate_default_settings(self):
        """This method will notify the default ACL settings on printer"""
        try:
            self.__acl_get_operation()
            if self.default == self.response:
                print 'Printer has the default settings- Validation Successfull'
            else:
                raise AssertionError("Printer has not default ACL settings")
        except Exception, msg:
            raise  AssertionError(msg)

    def get_acl_state(self):
        """This method is used to get the status of aclEnabled"""
        try:
            self.__acl_get_operation()
            print "The values of acl state is:", self.response['aclEnabled']
            return self.response['aclEnabled']
        except Exception, msg:
            raise AssertionError("Error in getting acl state -> %s" % str(msg))


    def change_acl_state(self, state, status_code = '200'):
        """This method will change the aclEnabled option either to true or false. True means enable and false means disable.
        Arguments: The keyword takes 2 arguments
        | Argument 1 | |Argument 2 |
        |  state     |  | status_code|"""

        self.__acl_get_operation()
        if self.response['aclEnabled'] == state:
            print 'The ACL state is already %s'%state
        else:
            self.response['aclEnabled'] = state
            try:
                self.__acl_put_operation(self.response, int(status_code))
            except Exception, msg:
                raise AssertionError(msg)

    def validate_acl_state(self, state):
        """This keyword is used to valiadte the ACL state after modififying the ACL state.
        This keyword takes 1 argument.
        | Argument 1 |
        |  state  |   """
        try:
            self.__acl_get_operation()
        except Exception, msg:
            raise AssertionError(msg)

        print "Value of acl state is:", self.response['aclEnabled']
        if self.response['aclEnabled'] == state:
            print 'The ACL state updated successfully'
        else:
            raise AssertionError("ACL state validation failed")

    def get_httpBypass_state(self):
        """This method is used to know the status of httpbypass"""
        try:
            self.__acl_get_operation()
            print "The values of httpbypass is:", self.response['httpBypassEnabled']
            return self.response['httpBypassEnabled']
        except Exception, msg:
            raise AssertionError("Error in getting httpbypass state -> %s" % str(msg))

    def change_httpBypass_state(self, state, status_code = '200'):
        """This method will change the httpBypass option either to true or false. True means enabele and false means disable.
                Arguments: The keyword takes 2 arguments
                | Argument 1 | |Argument 2 |
                |  state     |  | status_code| """
        self.__acl_get_operation()
        if self.response['httpBypassEnabled'] == state:
            print 'The httpBypassEnabled state is already %s'%state
        else:
            self.response['httpBypassEnabled'] = state
            try:
                self.__acl_put_operation(self.response, int(status_code))
            except Exception, msg:
                raise AssertionError(msg)


    def validate_httpBypass_state(self, state):
        """This keyword is used to valiadte the httpBypass state after modififying the httpBypass state.
                This keyword takes 1 argument.
                | Argument 1 |
                |  state  |   """
        try:
            self.__acl_get_operation()
        except Exception, msg:
            raise AssertionError(msg)
        print "Value of httpBypassEnabled state is:", self.response['httpBypassEnabled']
        if self.response['httpBypassEnabled'] == state:
            print 'The httpBypassEnabled state updated successfully'
        else:
            raise AssertionError("httpBypassEnabled state validation failed")

    def create_rule(self, exp_resp_code='200', ipv4Address=None, subnet=None, rulestatus=None, validation='True'):
        """This method is used to create ACL rules on printer.
                        Arguments: The keyword takes 4 arguments
                        | Argument 1 |     |Argument 2 | |Argument 3 | | Argument 4 |
                        |  exp_resp_code|  | ipv4Address| | subnetmask| | rule_status | """
        if ipv4Address == None:
            hostname = socket.gethostname()
            client_ip = socket.gethostbyname(hostname)
            ip_split = client_ip.split('.')
            del ip_split[-1]
            ip_split.append(str(random.randint(1, 223)))
            ipv4Address = ('.').join(ip_split)
            self.ipv4Address = ipv4Address
        elif ipv4Address == 'client_ip':
            hostname = socket.gethostname()
            self.ipv4Address = socket.gethostbyname(hostname)
        else:
            self.ipv4Address = ipv4Address
        if subnet is None:
            subnetMask = '255.255.255.0'
        else:
            subnetMask = subnet
        if rulestatus is None:
            rule_status = 'true'
        else:
            rule_status = rulestatus
        self.__acl_get_operation()
        rule_list = []
        if self.response.has_key('aclRules'):
            rule_list = self.response['aclRules']
        rule = {'ipv4Address': self.ipv4Address, 'subnetMask': subnetMask, 'ruleEnabled': rule_status}
        rule_list.append(rule)
        self.response['aclRules'] = rule_list

        self.__acl_put_operation(self.response, int(exp_resp_code))
        self.put_payload = self.response
        print self.put_payload
        print self.response

        if validation == 'True':
            self.__acl_get_operation()
            if self.put_payload == self.response:
                print "ACL Create rule validation is successful"
            else:
                raise AssertionError("ACL Create rule validation is not successful")

    def validate_rules_after_powercycle(self):
        """This keyword will validate the ACL state of the printer after powercycle"""
        response = requests.get(self.uri)
        value=response.json()
        print value
        if value==self.put_payload:
            print "ACL rules reamins constant after power cycle"
        else:
            raise AssertionError("ACL rules changed after power cycle")


    def validate_missing_key_in_payload(self,key):
        """This keyword is used to validate printer response while giving payload without key.
        It takes 1 argument.  | Argument 1 |
                               | key   |   """
        try:
            payload = self.default
            del payload[key]
            print "The value of payload is:", payload
            self.__acl_put_operation(payload, 400)
        except Exception, msg:
            raise AssertionError("Unable to copy file -> %s" % str(msg))

    def validate_missing_value_in_payload(self,key,value):
        """This keyword is used to valiadte printer response while giving missing payload
        It takes 2 arguments.
        |Argument 1|  |Argumrnt 2|
         | key     |   | value |   """
        try:
            payload = self.default
            payload[key]=value
            print "The value of payload is:", payload
            self.__acl_put_operation(payload, 400)
        except Exception, msg:
            raise AssertionError("Unable to copy file -> %s" % str(msg))

    def send_empty_payload(self):
        """This keyword is used to validate printer response while giving empty payload."""
        try:
            payload = self.default
            payload.clear()
            print "Value of payload is:",payload
            self.__acl_put_operation(payload, 400)
        except Exception, msg:
            raise AssertionError("Unable to copy file -> %s" % str(msg))

    def delete_acl_rule(self, rule_num):
        """This keyword is used to delete individual acl rule.
        It takes 1 argument.
        | Argument 1|
        | rule_num   |"""
        try:
            rule_num_to_delete = int(rule_num) - 1
            self.__acl_get_operation()
            self.response['aclRules'].pop(rule_num_to_delete)
            self.__acl_put_operation(self.response)
            print "Response value is:",self.response
        except Exception, msg:
            raise AssertionError("Unable to delete acl rule -> %s" % str(msg))

    def delete_all_acl_rule(self):
        """This keyword is used to delete all acl rule."""
        try:
            self.__acl_get_operation()
            self.response['aclRules']=[]
            self.__acl_put_operation(self.response)
            print "Response value is:",self.response
        except Exception, msg:
            raise AssertionError("Unable to delete all acl rules -> %s" % str(msg))

    def post_response_validation(self):
        """This keyword is used to valiadte the post operation. Printer does not supports post operation. """
        try:
            post_response = requests.post(self.uri, headers=self.headers, data=json.dumps(self.default))
            if post_response.status_code == 405:
                print "Invalid post method validation is successful"
            else:
                raise AssertionError("Printer accepts post operation")
        except Exception, msg:
            raise AssertionError("post response validation is not successful -> %s" % str(msg))


    def disable_interface(self,interface):
        """This keyword will disable the network interface of the test PC.
                It takes 1 argument.
                | Argument 1|
                | interface   |"""
        try:
            cmd = 'netsh interface set interface "' + interface + '" admin=disable'
            subprocess.check_output(cmd, shell=True)
        except Exception, msg:
            raise AssertionError("post response validation is not successful -> %s" % str(msg))
        
    def enable_interface(self,interface ):
        """This keyword will enable the network interface of the test PC.
                        It takes 1 argument.
                        | Argument 1|
                        | interface   |"""
        try:
            cmd = 'netsh interface set interface "' + interface + '" admin=enable'
            subprocess.check_output(cmd, shell=True)
        except Exception, msg:
            raise AssertionError("post response validation is not successful -> %s" % str(msg))


# **************** Private Methods ******************************

    def __acl_put_operation(self, payload, response_code=200):
        """This keyword will do the put operation on printer.
        It takes 2 arguments.
        | Argument 1|  | Argument 1|
        | Payload   |  | response code   | """
        try:
            put_response = requests.put(self.uri, headers=self.headers, data=json.dumps(payload))
            print payload
        except Exception, msg:
            raise AssertionError(msg)

        if put_response.status_code != response_code:
            raise AssertionError("Unexpected ACL Put Operation - Expected response code = %s :: Actual response code = %s" % (response_code, put_response.status_code))
        else:
            print "ACL Put operation and validation is successful"


    def __acl_get_operation(self, response_code=200):
        """This keyword will do the get operation on printer.
        It takes 1 argument.
        | Argument 1|
        | response_code   |"""
        try:
            self.response = requests.get(self.uri)
        except Exception, msg:
            raise AssertionError(msg)
        if self.response.status_code != response_code:
            raise AssertionError("Unexpected ACL Get Operation - Expected response code = %s :: Actual response code = %s" % (response_code,self.response.status_code))
        else:
            self.response = self.response.json()
            print "ACL Get operation and validation is successful"








































