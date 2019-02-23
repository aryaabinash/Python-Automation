import netmiko

class SwitchKeywords():
    def __init__(self,switch_ip):
        self.switch_ip = switch_ip

    def enable_port_as_authenticated(self, port):
        """
        Will generate the command to be executed for making the port as Authenticated Port and
        will call the method to execute the same
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Port Number  |
        """
        print 'Enabling the port ' + str(port) +' as Authenticated port'
        command = 'aaa port-access authenticator ' + str(port)

        try:
            self.__exec_switch_config_command(command)
            print 'Successfully enabled the port ' + str(port) +' as Authenticated port'
            
        except Exception, msg:
            raise AssertionError("Failed to enable the Port %s as Authenticated Port -> %s" %(str(port), str(msg)))

    def enable_port_as_non_authenticated(self, port):
        """
        Will generate the command to be executed for making the port as Non Authenticated Port and
        will call the method to execute the same
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Port Number  |
        """
        print 'Enabling the port ' + str(port) +' as Non-Authenticated port'
        command = 'no aaa port-access authenticator ' + str(port)

        try:
            self.__exec_switch_config_command(command)
            print 'Successfully enabled the port ' + str(port) +' as Non-Authenticated port'
                                 
        except Exception, msg:
            raise AssertionError("Failed to enable the Port %s as Non-Authenticated Port -> %s" %(str(port), str(msg)))

    def enable_port(self, port):
        """
        Will generate the command to be executed for enabling the port and  will call the method to execute the same
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Port Number  |
        """
        print 'Enabling the port ' + str(port)
        command = 'interface ethernet ' + str(port) +' enable' 

        try:
            self.__exec_switch_config_command(command)
            print 'Successfully enabled the port ' + str(port)
                                 
        except Exception, msg:
            raise AssertionError("Failed to enable the Port %s-> %s" %str(port))

    def disable_port(self, port):
        """
        Will generate the command to be executed for disabling the port and  will call the method to execute the same
        Arguments: The keyword takes 1 argument.
        | Argument 1   |
        | Port Number  |
        """
        print 'Disabling the port ' + str(port)
        command = 'interface ethernet ' + str(port) +' disable' 

        try:
            self.__exec_switch_config_command(command)
            print 'Successfully disabled the port ' + str(port)
                                 
        except Exception, msg:
            raise AssertionError("Failed to disable the Port %s-> %s" %str(port))
        

    def __exec_switch_config_command(self, cmd):
        # Method will establish a connection with switch and execute the command passed in Config mode
        try:
            connection = netmiko.ConnectHandler(ip = self.switch_ip, device_type = 'hp_procurve')
            connection.send_config_set(cmd)
            connection.disconnect()          
                                 
        except Exception, msg:
            raise AssertionError(msg)
        




       
