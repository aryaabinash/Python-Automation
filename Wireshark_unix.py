import threading
import subprocess
import platform
import time
import os
from NetworkLibrary.BaseOperations.BaseWiresharkOperation import BaseWiresharkOperation



class Wireshark(BaseWiresharkOperation):

    def __init__(self):
        self.file_name = ''
        self.command = ''

    def start_wireshark_capture(self, file_name, password='q1w2e3r4', interface='', ws_filter=''):
        try:
            self.file_name = file_name
            print file_name

            if not os.path.exists(self.file_name + '.pcap'):
                self.command = 'echo "" > ' + self.file_name + '.pcap'
                print "the command is", self.command
                self.execute_cmd()
                print self.execute_cmd()
                time.sleep(2)
                print "changing the permission of file"
                self.command = 'echo "q1w2e3r4" | sudo -S chmod -R 0777 ' + self.file_name + '.pcap'
                print self.command
                self.execute_cmd()
                time.sleep(2)

            self.command = ' echo ' + '"' + password + '" ' + ' | ' + ' sudo ' + ' -S ' + ' tshark ' + ' -i ' + interface + ' -f ' + '"' + ws_filter + '"' + ' -w ' + self.file_name + '.pcap -q'                                                                                                                                                                                        ' '
            print self.command

            print 'Executing ' + self.command + 'to start Wireshark Capture'
            self.wireshark_capture = threading.Thread(target=self.execute_cmd)
            self.wireshark_capture.start()

        except Exception, msg:
            raise AssertionError("Failed to start wireshark capture -> %s" % str(msg))

        print '*********** Wireshark Capture Started ***********'


    def stop_wireshark_capture(self, wireshark_folder):

        print 'Stopping Wireshark capture'

        try:
            if platform.system() == 'Linux':
                self.command = ' echo "q1w2e3r4" | sudo -S killall -9 dumpcap'
                print self.command
                self.execute_cmd()
                self.command = 'echo "q1w2e3r4" | sudo -S chmod -R 0777 ' + wireshark_folder
                print self.command
                self.execute_cmd()

            else:
                self.command = 'Taskkill /IM dumpcap.exe /T /F'
                self.execute_cmd()

            self.wireshark_capture.join()

        except Exception, msg:
            raise AssertionError("Failed to stop wireshark capture -> %s" %str(msg))

        print '*********** Wireshark Capture Stopped ***********'
        print ' Wireshark Capture File : ' + self.file_name + '.pcap'

    def convert_cap_to_txt_file(self):
        if not os.path.exists(self.file_name + '.txt'):
            self.command= 'echo "" > ' + self.file_name+'.txt'
            self.execute_cmd()

        print 'Converting ' + self.file_name + '.pcap to ' + self.file_name + '.txt'
        self.command = 'echo "q1w2e3r4" | sudo -S chmod -R 0777 ' + self.file_name + '.txt'
        print self.command
        self.execute_cmd()
        self.command = 'tshark -r ' + self.file_name + '.pcap -t ad > ' + self.file_name + '.txt'
        try:
            self.execute_cmd()
            print 'pcap file converted to txt file'
        except Exception, msg:
            raise AssertionError("Failed to convert pcap to text file-> %s" %str(msg))

    def execute_cmd(self):

        try:
            subprocess.check_output(str(self.command), shell=True)
            time.sleep(5)
        except Exception, msg:
            print msg




