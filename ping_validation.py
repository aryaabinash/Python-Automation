import subprocess
import platform
import time
import random

class PrinterSetup:

    def __init__(self, ipv4):
        self.ipv4 = ipv4
        print self.ipv4


    def ping_validation(self):
        OS_name = platform.system()

        print '\n*********************** Ping Validation ***********************\n'
        if OS_name == 'Windows':
            command = "ping " + str(self.ipv4)

        elif OS_name == 'Linux':
            command = "ping " + str(self.ipv4) + ' -c 4'
            if ':' in self.ipv4:
                print self.ipv4
                command = "ping6" + ' ' + str(self.ipv4) + ' -c 4'
                print command


        count = 0
        ping_flag = False
        try:
            while (count < 5):
                ping_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                print ping_output

                if "TTL" in ping_output or "ttl" in ping_output or "time=" in ping_output:
                    print "Ping to Printer Successful"
                    ping_flag = True
                    break

                elif "TTL" not in ping_output or "ttl" not in ping_output or 'time=' not in ping_output:
                    print "Ping to Printer Failed - Attempt %d " % (count + 1)
                    ping_flag = False
                    time.sleep(60)
                count += 1

            if ping_flag is False:
                print "Printer with IP - %s is not reachable" % self.ipv4

            return ping_flag

        except Exception, msg:
            ping_flag = False
            print self.ipv4, msg
            print("Printer Out of network")
            return ping_flag
        finally:
            print '\n***************************************************************\n'