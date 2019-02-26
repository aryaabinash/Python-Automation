#################### Headers ########################

import os
import datetime
import time
import sys

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import xml.etree.ElementTree as ET


################## Class: Keyword library ####################

class WebKeywords:
    def __init__(self):
        self.printer_ip = ''
        self.current_page = ''
        self.tree = ''
        self.root = ''
        self.browser = ''
        self.driver = ''
        self.root_folder = ''
        self.screen_capture_path = ''
        self.capture_file = ''

    def ews_initialize(self, printerip, sitemap_file, browser_type, root_folder):

        """
        Initialize the variables for driver initialization and sitemap parsing

        Arguments: The keyword takes 3 arguments.
        | Argument 1 | Argument 2      | Argument 3      |
        | Printer IP | Sitemap Path    | Browser    Type |

        """
        self.printer_ip = printerip
        if ':' in self.printer_ip:
            self.printer_ip = '['+printerip+']'
        self.current_page = ''


        self.root_folder = root_folder
        self.screen_capture_path = os.path.join(self.root_folder, "Logs", "Ews_Screen_Captures")
        self.capture_file = ''

        if not os.path.exists(self.screen_capture_path):
            os.makedirs(self.screen_capture_path)
        
        try:
            self.tree = ET.parse(sitemap_file)
            self.root = self.tree.getroot()
        except:
            raise AssertionError("Error in Parsing the Sitemap XML")

        self.browser = browser_type

        # Applicable for Linux environment
        # self.__reset_proxy_settings()

    def ews_open_browser(self):
        """
        Initialize the driver based on the browser type and will open the browser

        """
        if self.browser == 'firefox':
            try:
                print 'Opening the firefox browser'
                profile = webdriver.FirefoxProfile()
                profile.accept_untrusted_cert = True
                myproxy = ""
                proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': myproxy, 'noProxy': ''})
                if 'win' in sys.platform :
                    platform = "firefox_win"
                else:
                    platform = "firefox24_linux"
                path = os.path.dirname(os.path.abspath(__file__))
                binary = FirefoxBinary(os.path.join(path,platform,"firefox"))
                self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, proxy=proxy)
                print 'Successfully launched firefox browser'

            except:
                raise AssertionError("Unable to Initialize the firefox browser")

        elif self.browser == 'chrome':
            try:
                print 'Opening the Chrome browser'

                path = os.path.dirname(os.path.abspath(__file__))
                if 'win' in sys.platform :
                    self.driver = webdriver.Chrome(os.path.join(path, "win_chromedriver"))
                else:
                    self.driver = webdriver.Chrome(os.path.join(path, "lin_chromedriver"))

                print 'Successfully launched Chrome browser'

            except:
                raise AssertionError("Unable to Initialize the chrome browser")

        elif self.browser == 'safari':
            pass
        else:
            raise AssertionError("Unsupported Browser")

    def ews_close_browser(self):
        """
        Closing the browser

        """
        try:
            print 'Closing the browser'
            self.driver.quit()
            print 'Successfully Closed the browser'

        except:
            raise AssertionError("Unable to Quit the browser")

    def ews_navigate_to_page(self, page_element, conn_type):
        """
        Navigate to the page with provided Page Key and Connection type

        Arguments: The keyword takes 2 arguments.
        | Argument 1 | Argument 2       |
        | Page Key   | Connection Type  |

        """
        try:
            print 'Navigating to the Page %s'%(page_element)

            # Search for element in sitemap should happen only in the current page section
            self.current_page = page_element
            self.capture_file = page_element

            page_path = self.__get_page_path(page_element)
            self.driver.set_page_load_timeout(30)
            self.driver.get(conn_type + '://' + self.printer_ip + '/' + page_path)

            time.sleep(20)
            print 'Successfully Navigated to the page %s'%(page_element)

        except TimeoutException:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to load the EWS - Timedout")

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to Navigate to Page - Error : %s" % msg)

    def ews_navigate_to_page_with_credentials(self, page_element, conn_type, username, password):
        """
        Navigate to the page with authentication using provided Page Key, Connection type, Username and Password

        Arguments: The keyword takes 4 arguments.
        | Argument 1 | Argument 2       | Argument 3 | Argument 4  |     
        | Page Key   | Connection Type  | Username   | Password    |

        """
        try:
            print 'Navigating to the Page %s'%(page_element)

            # Search for element in sitemap should happen only in the current page section
            self.current_page = page_element
            self.capture_file = page_element

            page_path = self.__get_page_path(page_element)
            self.driver.set_page_load_timeout(30)
            self.driver.get(conn_type + '://' + username + ':' + password + '@' +self.printer_ip + '/' + page_path)

            time.sleep(20)
            print 'Successfully Navigated to the page with credentials %s'%(page_element)

        except TimeoutException:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to load the EWS(With credentials) - Timedout")

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to Navigate to Page(With credentials) - Error : %s" % msg)

    def ews_click_button(self, element_key):
        """
        Clicks Radio/button with provided key

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Clicking the button - %s'%(element_key)
            element = self.__get_element_id(element_key)
            element.click()
            time.sleep(5)
            print 'Successfully clicked the button - %s'%(element_key)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to Click the button - Error : %s" % msg)

    def ews_check_checkbox(self, element_key):
        """
        Check the checkbox with provided key

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Checking the Checkbox - %s' % (element_key)
            if not self.ews_checkbox_ischecked(element_key):
                element = self.__get_element_id(element_key)
                element.click()
                time.sleep(5)
            print 'Successfully Checked the checkbox - %s' % (element_key)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to Check the Checkbox - Error : %s" % msg)

    def ews_uncheck_checkbox(self, element_key):
        """
        Uncheck the checkbox with provided key

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Unchecking the Checkbox - %s' % (element_key)
            if self.ews_checkbox_ischecked(element_key):
                element = self.__get_element_id(element_key)
                element.click()
                time.sleep(5)
            print 'Successfully Unchecked the checkbox - %s' % (element_key)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to UnCheck the Checkbox - Error : %s" % msg)

    def ews_checkbox_ischecked(self, element_key):
        """
        Check whether Checkbox is checked

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Checking whether checkbox - %s - is Enabled'%(element_key)
            time.sleep(5)
            element = self.__get_element_id(element_key)
            checkbox_status = element.is_selected()
            print 'Status of Checkbox (%s)(True if enable,else false) - %r'%(element_key,checkbox_status)
            return checkbox_status

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to retrieve the status of Checkbox - Error : %s" % msg)

    def ews_set_text(self, element_key, text):
        """
        Set value in the Textbox

        Arguments: The keyword takes 2 arguments.
        | Argument 1    | Argument 2  |
        | Element Key   | Value       |

        """
        try:
            print 'Setting the value (%s) in Textbox - %s' % (text,element_key)
            element = self.__get_element_id(element_key)
            element.clear()
            element.send_keys(text)
            time.sleep(5)
            print 'Successfully set the value in Textbox'

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to set value in textbox - Error : %s" % msg)

    def ews_get_text(self, element_key):
        """
        Get value in the Textbox

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Getting the value from Textbox - %s' % (element_key)
            element = self.__get_element_id(element_key)
            print 'Value retrieved from Textbox - %s'%(element.get_attribute('value'))
            return element.get_attribute('value')

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to get value from textbox - Error : %s" % msg)

    def ews_clear_text(self, element_key):
        """
        Clears the Textbox

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Clearing the Textbox - %s'%(element_key)
            element = self.__get_element_id(element_key)
            element.clear()
            time.sleep(2)
            print 'Successfully cleared the Textbox - %s'%(element_key)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to clear value in textbox - Error : %s" % msg)

    def ews_dropdown_select_by_text(self, element_key, value):
        """
        Select the value from the Dropdown

        Arguments: The keyword takes 2 arguments.
        | Argument 1    | Argument 2  |
        | Element Key   | Value       |

        """
        try:
            print 'Selecting Text from dropdown box'
            element = Select(self.__get_element_id(element_key))
            element.select_by_value(value)
            time.sleep(5)
            print 'Successfully selected (%s) in dropdown box'%(value)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to select the text in dropdown - Error : %s" % msg)

    def ews_table_select_by_text(self, element_key, column_num, identifier):
        """
        Select the value from the Table

        Arguments: The keyword takes 2 arguments.
        | Argument 1    | Argument 2     | Argument 3   |
        | Element Key   | Column Number  | Search value |

        """

        try:
            print 'Selecting Radio from table using the value (%s)'%(identifier)
            element = self.__get_element_id(element_key)
            table_rows = element.find_elements_by_tag_name("tr")
            data = []

            for row in table_rows:
                columns = row.find_elements_by_tag_name("td")
                col_list = []
                for col in columns:
                    col_list.append(col)
                data.append(col_list)
            data = data[1:]
            i = 1
            for index in range(0, len(data)):
                if data[index][column_num].text.strip() == identifier:
                    element = data[index][0].find_elements_by_tag_name("input")[0]
                    element.click()
                    break
                else:
                    i = i + 1
            time.sleep(5)
            print 'Successfully selected (%s) in table' % (identifier)
        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to select text in table - Error : %s" % msg)

    def ews_get_field_value(self, element_key):
        """
        Get value from field in the EWS Page

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Getting the value from field - %s' % (element_key)
            element = self.__get_element_id(element_key)
            print 'Value retrieved from Textbox - %s' % (element.text)
            return element.text

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to get value from field - Error : %s" % msg)


    def ews_is_element_present(self, element_key):
        """
        Checks whether the particular element is present in the current page

        Arguments: The keyword takes 1 argument.
        | Argument 1    |
        | Element Key   |

        """
        try:
            print 'Checking whether the element - %s - is present in the current page' % (element_key)
            element = self.__get_element_id (element_key)
            return True

        except:
            self.ews_capture_screen()
            self.ews_close_browser()
            return False

    def ews_browse_file(self, element_key, file_path):
        """
        Browse the file and Select the same

        Arguments: The keyword takes 1 argument.
        | Argument 1    | Argument 1    |
        | Element Key   | File path   |

        """
        try:
            print 'Browsing the file and selecting the same'
            element = self.__get_element_id(element_key)
            element.send_keys(file_path)
            print 'File -  %s - Successfully selected ' % (file_path)

        except Exception, msg:
            self.ews_capture_screen()
            self.ews_close_browser()
            raise AssertionError("Unable to browse the file - Error : %s" % msg)

    def ews_capture_screen(self):
        """
        Capture the current screen and saved in the Logs location
        """
        try:
            time_stamp = time.time()
            format_ts = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y_%m_%d_%H_%M_%S')
            self.capture_file = os.path.join(self.screen_capture_path,self.capture_file + '_' + format_ts + '.png')
            print '-' * 15
            print 'ERROR: The Screen Capture is saved in the location \n%s' % self.capture_file
            print '-' * 15
            self.driver.save_screenshot(self.capture_file)

        except Exception, msg:
            self.ews_close_browser()
            raise AssertionError("Unable to capture screen : %s" % msg)
        

        ################## Private methods #####################

    def __get_element_id(self, _element):
        """
        Returns the element identifier by parsing the Sitemap xml. This will search in the order id, name, xpath,
        class, type. Searching will be done only in the Page Section mentioned in current_page variable
        
        """
        try:
            sitemap_element = ''
            _page = self.current_page
            for page in self.root.getiterator('Page'):
                if page.attrib['key'] == _page:
                    for element in page.getiterator('Element'):
                        if element.attrib['key'] == _element:
                            if element.attrib['id']:
                                sitemap_element = element.attrib['id']
                                return self.driver.find_element_by_id(element.attrib['id'])
                            elif element.attrib['name']:
                                sitemap_element = element.attrib['name']
                                return self.driver.find_element_by_name(element.attrib['name'])
                            elif element.attrib['xpath']:
                                sitemap_element = element.attrib['xpath']
                                return self.driver.find_element_by_xpath(element.attrib['xpath'])
                            elif element.attrib['class']:
                                sitemap_element = element.attrib['class']
                                return self.driver.find_element_by_class_name(element.attrib['class'])
                            elif element.attrib['type']:
                                sitemap_element = element.attrib['type']
                                return self.driver.find_element_by_type(element.attrib['type'])
                            else:
                                return ''

        except NoSuchElementException:
            raise AssertionError(
                "Element (%s - %s) not found in the page - %s" % (_element, sitemap_element, self.current_page))

        except:
            raise AssertionError("Error in Parsing Sitemap Xml to get the element identifier")

    def __get_page_path(self, page_element):
        """
        Returns the relative path for page_element by parsing the Sitemap xml
        """
        try:
            for page in self.root.getiterator('Page'):
                if page.attrib['key'] == page_element:
                    return str(page.attrib['relative_path'])

        except:
            raise AssertionError("Error in Parsing Sitemap Xml to get the Relative Page")

    def __reset_proxy_settings(self):
        """
        Removes all the proxy settings
        """
        try:
            os.system("unset http_proxy")
            os.system("unset HTTP_PROXY")
            os.system("unset https_proxy")
            os.system("unset HTTPS_PROXY")
            os.system("unset no_proxy")
            os.system("unset NO_PROXY")
            os.system("unset ftp_proxy")
            os.system("unset FTP_PROXY")

        except:
            raise AssertionError ("Error in removing proxies")





