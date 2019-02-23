import threading
import subprocess
import platform
import time


class Wireshark:

    def __init__(self):
        self.file_name = ''
        self.command = ''

    def start_wireshark_capture(self, file_name, ws_filter=''):
        self.file_name = file_name
        self.command = 'tshark ' + ws_filter + '-w ' + self.file_name + '.pcap -q'
        print 'Executing ' + self.command + 'to start Wireshark Capture'

        try:
            self.wireshark_capture = threading.Thread(target=self.__execute_command)
            self.wireshark_capture.start()
            
        except Exception, msg:
            raise AssertionError("Failed to start wireshark capture -> %s" %str(msg))
                                 
        print '*********** Wireshark Capture Started ***********'

    def stop_wireshark_capture(self, wireshark_folder):
        print 'Stopping Wireshark capture'

        try:       
            if platform.system() == 'Linux':
                self.command = 'killall -9 dumpcap'                   
                self.__execute_command()
                self.command = "chmod -R 0777 " + wireshark_folder
                self.__execute_command()
    
            else:
                self.command = 'Taskkill /IM dumpcap.exe /T /F'
                self.__execute_command()

            self.wireshark_capture.join()
            
        except Exception, msg:
            raise AssertionError("Failed to stop wireshark capture -> %s" %str(msg))
                                 
        print '*********** Wireshark Capture Stopped ***********'
        print ' Wireshark Capture File : ' + self.file_name + '.pcap'        

    def convert_cap_to_txt_file(self):
        print 'Converting ' + self.file_name + '.pcap to ' + self.file_name + '.txt'
        self.command = 'tshark -r ' + self.file_name + '.pcap -t ad > ' + self.file_name + '.txt'
        try:
            self.__execute_command()
            print 'pcap file converted to txt file'
            
        except Exception, msg:
            raise AssertionError("Failed to convert pcap to text file-> %s" %str(msg))                        
        
    def __execute_command(self):
        try:
            subprocess.check_output(str(self.command), shell=True)
            time.sleep(5)
        except Exception, msg: 
            print msg

