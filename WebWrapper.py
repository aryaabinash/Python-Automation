from Packages.Interfaces.EWS.EWSKeywords import *


class WebWrapper:
    def __init__(self, printerip, sitemapfile, browser_type, root_folder, username, password , Signinelement):
        self.printer_ip = printerip
        self.sitemap_file = sitemapfile
        self.browser_type = browser_type
        self.root_folder = root_folder
        self.username = username
        self.password = password
        self.Signinelement = Signinelement

        self.adapter = EWSKeywords()
        self.adapter.ews_initialize(self.printer_ip, self.sitemap_file, self.browser_type, self.root_folder, self.username, self.password, self.Signinelement)

    def ews_enable_wins_with_existing_values(self):
        """
        Configuring Wins in printer with Existing values without changing primary and secondary IP values

        """
        try:
            print 'Enabling WINS with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("WINS", "https")
            self.adapter.ews_click_button("WINS_Option_enable")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Enabled WINS using EWS'

        except Exception, msg:
            raise AssertionError("Unable to enable Wins -> %s" % msg)

    def ews_disable_wins(self):
        """
        Disabling wins in the printer

        """
        try:
            print 'Disabling WINS with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("WINS", "https")
            self.adapter.ews_click_button("WINS_Option_disable")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Disabled WINS using EWS'

        except Exception, msg:
            raise AssertionError("Unable to disable Wins -> %s" % msg)

    def ews_configure_wins_with_values(self, primary_ip=None, secondary_ip=None):
        """
        Configuring wins primary and secondary server IP address

        Arguments: The keyword takes 2 arguments.
        | Argument 1    | Argument 2    |
        | Primary IP    | Secondary IP  |

        """
        print 'Configuring WINS with values using EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("WINS", "https")
            self.adapter.ews_click_button("WINS_Option_enable")
            self.adapter.ews_clear_text("WINS_Primary_IP_0")
            self.adapter.ews_clear_text("WINS_Primary_IP_1")
            self.adapter.ews_clear_text("WINS_Primary_IP_2")
            self.adapter.ews_clear_text("WINS_Primary_IP_3")
            self.adapter.ews_clear_text("WINS_Secondary_IP_0")
            self.adapter.ews_clear_text("WINS_Secondary_IP_1")
            self.adapter.ews_clear_text("WINS_Secondary_IP_2")
            self.adapter.ews_clear_text("WINS_Secondary_IP_3")

            if primary_ip:
                a = primary_ip.split(".")
                self.adapter.ews_set_text("WINS_Primary_IP_0", a[0])
                self.adapter.ews_set_text("WINS_Primary_IP_1", a[1])
                self.adapter.ews_set_text("WINS_Primary_IP_2", a[2])
                self.adapter.ews_set_text("WINS_Primary_IP_3", a[3])

            if secondary_ip:
                b = secondary_ip.split(".")
                self.adapter.ews_set_text("WINS_Secondary_IP_0", b[0])
                self.adapter.ews_set_text("WINS_Secondary_IP_1", b[1])
                self.adapter.ews_set_text("WINS_Secondary_IP_2", b[2])
                self.adapter.ews_set_text("WINS_Secondary_IP_3", b[3])

            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully configured Wins with values using EWS'

        except Exception, msg:
            raise AssertionError("Unable to set the WINS values -> %s" % msg)

    def ews_get_wins_server_ip_address(self):
        """
        Retrive primary and secondary wins server address
        :return:
        """
        print 'Retrieving Wins primary and Secondary IP addresses'
        try:
            wins = []
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            wins.append(self.adapter.ews_get_field_value('WINS_Primary'))
            wins.append(self.adapter.ews_get_field_value('WINS_Secondary'))
            self.adapter.ews_close_browser()
            print 'Values retrieved '
            print wins
            return wins

        except Exception, msg:
            raise AssertionError("Unable to get WINS values -> %s" % msg)

    def ews_get_hostname(self):
        """
        Retrieve host name of the printer

        """
        try:
            print 'Retrieving Hostname using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Network_Identification", "https")
            hostname = self.adapter.ews_get_text("HostName")
            print 'Hostname retrieved : %s' % hostname
            self.adapter.ews_close_browser()
            return hostname

        except Exception, msg:
            raise AssertionError("Unable to retrieve HostName -> %s" % msg)

    def ews_set_hostname(self, hostname):
        """
        Set Hostname in Printer

        Arguments: The keyword takes 1 arguments.
        | Argument 1   |
        | Hostname     |

        """
        try:
            print 'Setting Hostname through EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Network_Identification", "https")
            current_hostname = self.adapter.ews_get_text("HostName")
            self.adapter.ews_clear_text("HostName")
            self.adapter.ews_set_text("HostName", hostname)
            self.adapter.ews_click_button("Apply")
            if current_hostname != hostname:
                self.adapter.ews_click_button("Alert_Yes")
                time.sleep(120)
            self.adapter.ews_close_browser()
            print 'Successfully set the new hostname : %s' % hostname

        except Exception, msg:
            raise AssertionError("Unable to Set the HostName -> %s" % msg)

    def ews_restore_network_defaults(self):
        """
        Performing Network Defaults

        """
        try:
            print 'Restoring Network Defaults using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("NetworkDefaults", "https")
            self.adapter.ews_click_button("RestoreNetworkDefaults")
            self.adapter.ews_click_button("yes")
            time.sleep(180)
            self.adapter.ews_close_browser()
            print 'Restoring Network Defaults using EWS completed successfully'

        except Exception, msg:
            raise AssertionError("Unable to perform restore network of the printer -> %s" % msg)

    def ews_powercycle_printer(self):
        """
        Performing PowerCycle/Reboot

        """
        try:
            print 'Rebooting the printer using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Power_Cycle", "https")
            self.adapter.ews_click_button("reboot")
            self.adapter.ews_click_button("Yes")
            time.sleep(180)
            self.adapter.ews_close_browser()
            print 'Printer rebooted successfully'

        except Exception, msg:
            raise AssertionError("Unable to reboot the printer -> %s" % msg)

    def ews_restore_factory_defaults(self):
        """
        Performing Restore factory defaults

        """
        try:
            print 'Restoring Factory Defaults using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("FactoryDefaults", "https")
            self.adapter.ews_click_button("RestoreFactoryDefaults")
            self.adapter.ews_click_button("yes")
            time.sleep(180)
            self.adapter.ews_close_browser()
            print 'Restoring Factory Defaults using EWS completed successfully'

        except Exception, msg:
            raise AssertionError("Unable to perform factory default the printer -> %s" % msg)

    def ews_enable_llmnr_on_printer(self):
        """
        Enabling LLMNR on Printer

        """
        try:
            print 'Enabling LLMNR through EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("LLMNR", "https")
            self.adapter.ews_click_button("LLMNR_Option_enable")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_click_button("Ok")
            self.adapter.ews_close_browser()
            print 'Successfully enabled LLMNR'

        except Exception, msg:
            raise AssertionError("Unable to enable LLMNR -> %s" % msg)

    def ews_disable_llmnr_on_printer(self):
        """
        Disabling LLMNR on Printer

        """
        try:
            print 'Disabling LLMNR through EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("LLMNR", "https")
            self.adapter.ews_click_button("LLMNR_Option_disable")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_click_button("Ok")
            self.adapter.ews_close_browser()
            print 'Successfully disabled LLMNR'

        except Exception, msg:
            raise AssertionError("Unable to disable LLMNR -> %s" % msg)

    def ews_configure_dns_server_with_values(self, preferred_ip=None, alternate_ip=None):
        """
        Configuring DNS with Preferred IP and Alternate IP address

        Arguments: The keyword takes 2 arguments.
        | Argument 1      | Argument 2    |
        | Preferred IP    | Alternate IP  |

        """
        try:
            print 'Configuring DNS with values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv4_Config", "https")
            self.adapter.ews_click_button("Manual_DNS_Server")
            self.adapter.ews_clear_text("PreferredDNS_0")
            self.adapter.ews_clear_text("PreferredDNS_1")
            self.adapter.ews_clear_text("PreferredDNS_2")
            self.adapter.ews_clear_text("PreferredDNS_3")
            self.adapter.ews_clear_text("AlternateDNS_0")
            self.adapter.ews_clear_text("AlternateDNS_1")
            self.adapter.ews_clear_text("AlternateDNS_2")
            self.adapter.ews_clear_text("AlternateDNS_3")

            if preferred_ip:
                a = preferred_ip.split(".")
                self.adapter.ews_set_text("PreferredDNS_0", a[0])
                self.adapter.ews_set_text("PreferredDNS_1", a[1])
                self.adapter.ews_set_text("PreferredDNS_2", a[2])
                self.adapter.ews_set_text("PreferredDNS_3", a[3])

            if alternate_ip:
                b = alternate_ip.split(".")
                self.adapter.ews_set_text("AlternateDNS_0", b[0])
                self.adapter.ews_set_text("AlternateDNS_1", b[1])
                self.adapter.ews_set_text("AlternateDNS_2", b[2])
                self.adapter.ews_set_text("AlternateDNS_3", b[3])

            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            self.adapter.ews_close_browser()
            print 'Successfully configured DNS with values using EWS'

        except Exception, msg:
            raise AssertionError("Unable to set DNS the values -> %s" % msg)

    def ews_get_dns_server_ip_address(self):
        """
        Retrive preferred and alternate dns server address and returns as a list

        """
        print 'Retrieving DNS preferred and alternate IP addresses'
        try:
            dns = []
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            dns.append(self.adapter.ews_get_field_value("DNS_IPv4Primary"))
            dns.append(self.adapter.ews_get_field_value("DNS_IPv4_Secondary"))
            self.adapter.ews_close_browser()
            print 'Values retrieved '
            print dns
            return dns

        except Exception, msg:
            raise AssertionError("Unable to get DNS values -> %s" % msg)

    def ews_get_dnsv6_server_ipv6_address(self):
        """
        Retrieving DNSv6 with Preferred IPv6 and Alternate IPv6 address

        """
        print 'Retrieving DNSv6 server Preferred_IPv6/Alternate_IPv6 through EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            preferred_dns_ipv6 = self.adapter.ews_get_field_value("DNS_IPv6_Primary")
            alternate_dns_ipv6 = self.adapter.ews_get_field_value("DNS_IPv6_Secondary")
            print '-------------------------------------------------------------------------------------------'
            print '  DNSv6 server Preferred_IPv6/Alternate_IPv6 Retrieved successfully '
            print '-------------------------------------------------------------------------------------------'
            self.adapter.ews_close_browser()
            dnsv6 = [preferred_dns_ipv6, alternate_dns_ipv6]
            dnsv6 = map(str, dnsv6)
            print 'Retrived dnsv6 from ews: '
            print dnsv6
            return dnsv6

        except:
            raise AssertionError("Unable to retrieve DNSv6 server Preferred_IPv6/Alternate_IPv6")

    def ews_set_dnsv6_server_ipv6_address(self, preferred_ipv6=None, alternate_ipv6=None):
        """
        Configuring DNS with Preferred IP and Alternate IP address

        Arguments: The keyword takes 2 arguments.
        | Argument 1      | Argument 2       |
        | Preferred IPv6  | Alternate IPv6   |

        """
        print 'Configuring DNSv6 with Preferred_IPv6/Alternate_IPv6 through EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv6_Config", "https")
            if preferred_ipv6:
                self.adapter.ews_set_text("PreferredDNSv6", preferred_ipv6)
            else:
                self.adapter.ews_clear_text("PreferredDNSv6")
            if alternate_ipv6:
                self.adapter.ews_set_text("AlternateDNSv6", alternate_ipv6)
            else:
                self.adapter.ews_clear_text("AlternateDNSv6")
            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            print '-------------------------------------------------------------------------------------------'
            print '  DNSv6 server Preferred_IPv6/Alternate_IPv6 Set successfully '
            print '-------------------------------------------------------------------------------------------'
            self.adapter.ews_close_browser()

        except:
            raise AssertionError("Unable to set DNSv6 server Preferred_IPv6/Alternate_IPv6")

    def ews_enable_snmp_v1v2_rw_access(self):
        """
        Enables SNMP Read Write Access

        """
        try:
            print 'Enabling SNMP v1v2 Read Write Access through EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("SNMP", "https")
            self.adapter.ews_click_button("Enable_v1v2_RW_access")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_click_button("OK")
            self.adapter.ews_close_browser()
            print 'Successfully enabled SNMP v1v2 RW Access'

        except Exception, msg:
            raise AssertionError("Failed to Enable SNMP v1v2 Read Write Access -> %s" % msg)

    def ews_set_ipconfig_to_dhcp(self):
        """
        Enables DHCP on printer

        """
        print 'Enabling DHCP through EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv4_Config", "https")
            self.adapter.ews_click_button("DHCP")
            self.adapter.ews_click_button("Apply")
            time.sleep(45)
            self.adapter.ews_click_button("OK")
            self.adapter.ews_close_browser()
            print 'Enabled DHCP through EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable DHCP through EWS -> %s" % msg)

    def ews_set_ipconfig_to_bootp(self):
        """
        Enables bootp on printer

        """
        print 'Enabling BOOTP through EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv4_Config", "https")
            self.adapter.ews_click_button("BOOTP")
            self.adapter.ews_click_button("Apply")
            time.sleep(45)
            self.adapter.ews_click_button("OK")
            self.adapter.ews_close_browser()
            print 'Enabled BOOTP through EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable BOOTP through EWS -> %s" % msg)

    def ews_set_ipconfig_to_autoip(self):
        """
        Enables AutoIP on printer

        """
        print 'Enabling Auto IP through EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv4_Config", "https")
            self.adapter.ews_click_button("AUTO_IP")
            self.adapter.ews_click_button("Apply")
            time.sleep(45)
            self.adapter.ews_click_button("OK")
            self.adapter.ews_close_browser()
            print 'Enabled Auto IP through EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable Auto IP through EWS -> %s" % msg)

    def ews_configure_manual_ip_with_values(self, ip_address=None, subnet_mask=None, default_gateway=None):
        """
        Configuring Manual Ip with values

        """
        try:
            print 'Configuring Manual Ip with values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPv4_Config", "https")
            self.adapter.ews_click_button("Manual_IP")
            self.adapter.ews_clear_text("IP_0")
            self.adapter.ews_clear_text("IP_1")
            self.adapter.ews_clear_text("IP_2")
            self.adapter.ews_clear_text("IP_3")
            self.adapter.ews_clear_text("Subnet_0")
            self.adapter.ews_clear_text("Subnet_1")
            self.adapter.ews_clear_text("Subnet_2")
            self.adapter.ews_clear_text("Subnet_3")
            self.adapter.ews_clear_text("Gateway_0")
            self.adapter.ews_clear_text("Gateway_1")
            self.adapter.ews_clear_text("Gateway_2")
            self.adapter.ews_clear_text("Gateway_3")

            if ip_address:
                a = ip_address.split(".")
                self.adapter.ews_set_text("IP_0", a[0])
                self.adapter.ews_set_text("IP_1", a[1])
                self.adapter.ews_set_text("IP_2", a[2])
                self.adapter.ews_set_text("IP_3", a[3])

            if subnet_mask:
                b = subnet_mask.split(".")
                self.adapter.ews_set_text("Subnet_0", b[0])
                self.adapter.ews_set_text("Subnet_1", b[1])
                self.adapter.ews_set_text("Subnet_2", b[2])
                self.adapter.ews_set_text("Subnet_3", b[3])

            if default_gateway:
                c = default_gateway.split(".")
                self.adapter.ews_set_text("Gateway_0", c[0])
                self.adapter.ews_set_text("Gateway_1", c[1])
                self.adapter.ews_set_text("Gateway_2", c[2])
                self.adapter.ews_set_text("Gateway_3", c[3])

            self.adapter.ews_click_button("Apply")
            time.sleep(45)
            self.adapter.ews_close_browser()
            print ' Configured Manual IP successfully ', ip_address, subnet_mask, default_gateway

        except Exception, msg:
            raise AssertionError("Unable to set the Manual IPv4 values -> %s" % msg)

    def ews_configure_network_protocol_enable_ipv4_only(self):
        try:
            print 'Enabling -IPv4 only- Option'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("NetProtocol", "https")
            self.adapter.ews_click_button("IPv4")
            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            self.adapter.ews_close_browser()
            print 'Successfully enabled -IPv4 only - Option'

        except:
            raise AssertionError("Unable to Enable IPv4 only in network protocols")

    def ews_configure_network_protocol_enable_ipv6_only(self):
        try:
            print 'Enabling -IPv6 only- Option'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("NetProtocol", "https")
            self.adapter.ews_click_button("IPv6")
            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            self.adapter.ews_close_browser()
            print 'Successfully enabled -IPv6 only - Option'

        except:
            raise AssertionError("Unable to Enable IPv6 only in network protocols")

    def ews_configure_network_protocol_enable_both_ipv4_ipv6(self):
        try:
            print 'Enabling -IPv4 and IPv6- Option'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("NetProtocol", "https")
            self.adapter.ews_click_button("IPv4v6")
            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            self.adapter.ews_close_browser()
            print 'Successfully enabled -IPv4 and IPv6 - Option'

        except:
            raise AssertionError("Unable to Enable both IPv4 and IPv6 in network protocols")

    def ews_install_id_certificate(self, cert_loc, password):
        """
        Installing ID Certificate
        """
        try:
            print 'Installing ID certificate using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("InstallCertificate", "https")
            self.adapter.ews_click_button("IDConfigure")
            self.adapter.ews_click_button("ImportCert")
            self.adapter.ews_click_button("CertificateNext")
            self.adapter.ews_browse_file("ImportIDFile", cert_loc)
            self.adapter.ews_set_text("PasswordID", password)
            self.adapter.ews_click_button("Finish")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'ID certifcate Installed successfully'

        except Exception as msg:
            raise AssertionError("Unable to install ID Certificate the printer -> %s" % msg)

    def ews_enable_ipv4_ipv6_using_ipv6(self, printer_ip_v6):
        """
        Enabling Both IPv4 and IPv6 option in Network Protocol Tab using IPV6 adddress
        """
        try:
            self.printer_ip_v6 = '[' + printer_ip_v6 + ']'
            self.adapter_v6 = EWSKeywords()
            self.adapter_v6.ews_initialize(self.printer_ip_v6, self.sitemap_file, self.browser_type, self.root_folder)

            print 'Enabling -IPv4 and IPv6- Option using IPv6 address'
            self.adapter_v6.ews_open_browser()
            self.adapter_v6.ews_navigate_to_page("NetProtocol", "https")
            self.adapter_v6.ews_click_button("IPv4v6")
            self.adapter_v6.ews_click_button("Apply")
            time.sleep(60)
            self.adapter_v6.ews_close_browser()
            print 'Successfully enabled -IPv4 and IPv6 - Option  using IPv6 address'

        except Exception as msg:
            raise AssertionError("Unable to enable -Both IPv4 and IPv6- option  using IPv6 address -> %s" % msg)

    def ews_change_printer_date_by_add_years(self,years):
        """
        Change printer date by adding years
        """
        try:
            print 'Changing printers date using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Date_And_Time", "https")
            if self.adapter.ews_checkbox_ischecked("DateTime_SyncNetwork"):
                self.adapter.ews_uncheck_checkbox("DateTime_SyncNetwork")
                self.adapter.ews_click_button("DateTime_SyncOk")
                self.adapter.ews_click_button("Apply")
                time.sleep(10)
            self.adapter.ews_close_browser()

            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Date_And_Time", "https")

            current_date = self.adapter.ews_get_text("CurrentDate")
            year = current_date.split('-')[2]
            new_year = int(str(year)) + int(years)

            self.adapter.ews_click_button("CurrentDate")
            self.adapter.ews_dropdown_select_by_text("Year_Selecter",str(new_year))
            self.adapter.ews_click_button("Date_Selecter")
            self.adapter.ews_click_button("Apply")
            self.adapter.ews_close_browser()
            print 'Successfully changed the date of printer using EWS'

        except Exception as msg:
            raise AssertionError("Unable to change the printer date -> %s" % msg)

    def ews_reset_printer_date(self):
        """
        Synchronizing printer time with computer time
        """
        try:
            print 'Resetting printer date using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Date_And_Time", "https")
            self.adapter.ews_click_button("DateTime_SyncComputer")
            time.sleep(15)
            self.adapter.ews_click_button("DateSettings_Apply")
            time.sleep(15)
            self.adapter.ews_close_browser()
            print 'Successfully synchronized printer date with computer using EWS'

        except Exception as msg:
            raise AssertionError("Unable to change the printer date -> %s" % msg)

    def ews_enable_dhcpv4_fqdn(self):
        """
        Enabling DHCPv4 FQDN in the printer

        """
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("DHCP", "https")
            self.adapter.ews_check_checkbox("Enable_DHCP_FQDN")
            self.adapter.ews_click_button("Apply")
            self.adapter.ews_close_browser()

        except:
            raise AssertionError("Unable to enable DHCPv4 fqdn")

    def ews_disable_dhcpv4_fqdn(self):
        """
        Disabling DHCPv4 FQDN in the printer

        """
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("DHCP", "https")
            self.adapter.ews_uncheck_checkbox("Enable_DHCP_FQDN")
            self.adapter.ews_click_button("Apply")
            self.adapter.ews_close_browser()
        except:
            raise AssertionError("Unable to disable DHCPv4 fqdn")

    def ews_verify_dhcpv4_fqdn_status_isEnabled(self):
        """
        Validate DHCPv4 FQDN status is enabled

        """
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("DHCP", "https")
            status = self.adapter.ews_checkbox_ischecked("Enable_DHCP_FQDN")
            if status == False:
                raise AssertionError("FQDN is disabled")
            self.adapter.ews_close_browser()

        except:
            raise AssertionError("Unable to check status DHCPv4 fqdn on EWS page")

    def ews_get_subnet_mask(self):
        """
        Retrive subnet mask of printer

        """
        print 'Retrieving Subnet Mask using EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            subnet_mask = self.adapter.ews_get_field_value("Subnet_Mask")
            self.adapter.ews_close_browser()
            print 'Subnet Mask retrieved : %s' % subnet_mask
            return subnet_mask

        except Exception, msg:
            raise AssertionError("Unable to retrieve Subnet Mask -> %s" % msg)

    def ews_get_default_gateway(self):
        """
        Retrive Default Gateway of printer

        """
        print 'Retrieving Default Gateway using EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            default_gateway = self.adapter.ews_get_field_value("Default_Gateway")
            self.adapter.ews_close_browser()
            print 'Default Gateway retrieved : %s' % default_gateway
            return default_gateway

        except Exception, msg:
            raise AssertionError("Unable to retrieve Default Gateway -> %s" % msg)

    def ews_get_domain_name(self):
        """
        Retrive Domain name of printer

        """
        print 'Retrieving Domain name using EWS'
        try:
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Wired_Status", "https")
            domain_name = self.adapter.ews_get_field_value("DomainName")
            self.adapter.ews_close_browser()
            print 'Domain name retrieved : %s' % domain_name
            return domain_name

        except Exception, msg:
            raise AssertionError("Unable to retrieve Domain name -> %s" % msg)

    def ews_set_domain_name(self, domain_name):
        """
        Set Domain name in Printer

        Arguments: The keyword takes 1 arguments.
        | Argument 1     |
        | Domain name    |

        """
        try:
            print 'Setting Domain name through EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Network_Identification", "https")
            self.adapter.ews_clear_text("DomainName")
            self.adapter.ews_set_text("DomainName", domain_name)
            self.adapter.ews_click_button("Apply")
            time.sleep(30)
            self.adapter.ews_close_browser()
            print 'Successfully set the new Domain name : %s' % domain_name

        except Exception, msg:
            raise AssertionError("Unable to Set the Domain name -> %s" % msg)

    def check_bonjour_printservices(self):
        # PrintService ={'P9100': 'True', 'IPP': 'True','LPD': 'True'}
        PrintService = []
        print 'this method will verify whether print services like P9100,IPP & LPD are present in the printer or not'
        try:
            self.adapter.ews_open_browser()
            try:
                self.adapter.ews_navigate_to_page("P9100", "https")
                if self.adapter.ews_is_element_present("Disable_TCP_Port_9100"):
                    PrintService.append("P9100")
            except:
                print 'P9100 Service is not available'
            self.adapter.ews_close_browser()

            self.adapter.ews_open_browser()
            try:
                self.adapter.ews_navigate_to_page("LPD", "https")
                if self.adapter.ews_is_element_present("DisableLPD_INK"):
                    PrintService.append("LPD")
            except:
                print 'LPD Service is not available'
            self.adapter.ews_close_browser()

            self.adapter.ews_open_browser()
            try:
                self.adapter.ews_navigate_to_page("IPP", "https")
                if self.adapter.ews_is_element_present("Enable_IPP"):
                    PrintService.append("IPP")
            except:
                print 'IPP Service is not available'
            self.adapter.ews_close_browser()
            if PrintService == []:
                raise AssertionError("No Print Services available")
            print PrintService
            return PrintService
        except Exception, msg:
            raise AssertionError("Unable to get the Required value-> %s" % msg)

    def ews_disable_bonjour(self):
        """
        Disabling bonjour in the printer

        """
        try:
            print 'Disabling Bonjour with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            self.adapter.ews_click_button("Disable_Bonjour")
            self.adapter.ews_click_button("Apply")
            self.adapter.ews_click_button("AlertYN")
            self.adapter.ews_close_browser()
            print 'Successfully Disabled Bonjour using EWS'
            time.sleep(30)

        except Exception, msg:
            raise AssertionError("Unable to disable Bonjour -> %s" % msg)

    def ews_enable_bonjour(self):
        """
        Disabling bonjour in the printer

        """
        try:
            print 'Disabling Bonjour with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            self.adapter.ews_click_button("Enable_Bonjour")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Disabled Bonjour using EWS'

        except Exception, msg:
            raise AssertionError("Unable to disable Bonjour -> %s" % msg)

    def ews_disable_IPP(self):
        """
        Disabling IPP in the printer

        """
        try:
            print 'Disabling IPP with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPP", "https")
            self.adapter.ews_uncheck_checkbox("Enable_IPP")
            self.adapter.ews_click_button("Apply")
            time.sleep(2)
            if self.adapter.ews_is_element_present("AlertYN"):
                self.adapter.ews_click_button("AlertYN")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Disabled IPP using EWS'

        except Exception, msg:
            raise AssertionError("Unable to disable IPP -> %s" % msg)

    def ews_enable_IPP(self):
        """
        Disabling IPP in the printer

        """
        try:
            print 'Enabling IPP with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("IPP", "https")
            self.adapter.ews_check_checkbox("Enable_IPP")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Enabled IPP using EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable IPP -> %s" % msg)

    def ews_disable_LPD(self):
        """
        Disabling LPD in the printer

        """
        try:
            print 'Disabling LPD with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("LPD", "https")
            self.adapter.ews_click_button("DisableLPD_INK")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Disabled LPD using EWS'

        except Exception, msg:
            raise AssertionError("Unable to disable LPD -> %s" % msg)

    def ews_enable_LPD(self):
        """
        Disabling LPD in the printer

        """
        try:
            print 'Enabling LPD with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("LPD", "https")
            self.adapter.ews_click_button("EnableLPD_INK")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully enabled LPD using EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable LPD -> %s" % msg)

    def ews_disable_P9100(self):
        """
        Disabling P9100 in the printer

        """
        try:
            print 'Disabling P9100 with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("P9100", "https")
            self.adapter.ews_click_button("Disable_TCP_Port_9100")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully Disabled LPD using EWS'

        except Exception, msg:
            raise AssertionError("Unable to disable LPD -> %s" % msg)

    def ews_enable_P9100(self):
        """
        Disabling P9100 in the printer

        """
        try:
            print 'Enabling P9100 with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("P9100", "https")
            self.adapter.ews_click_button("Enable_TCP_Port_9100")
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()
            print 'Successfully enabled LPD using EWS'

        except Exception, msg:
            raise AssertionError("Unable to Enable LPD -> %s" % msg)

    def ews_check_Bonjour_status(self):


        try:
            print 'Checking the status of Bonjour with existing values using EWS'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            BonjourStatus = self.adapter.ews_checkbox_ischecked("Enable_Bonjour")
            if BonjourStatus == False:
                self.adapter.ews_click_button("Enable_Bonjour")
                self.adapter.ews_click_button("Apply")
                time.sleep(10)
            self.adapter.ews_close_browser()

        except Exception, msg:
            raise AssertionError("Unable to Enable Bonjour -> %s" % msg)

    def ews_set_Bonjour_serviceName(self,bonjourservicename):
        """
        Disabling P9100 in the printer

        """
        try:
            print 'setting the Bonjour Service name'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            self.adapter.ews_set_text("Bonjour_Service_Name",bonjourservicename)
            self.adapter.ews_click_button("Apply")
            time.sleep(10)
            self.adapter.ews_close_browser()


        except Exception, msg:
            raise AssertionError("Unable to Enable LPD -> %s" % msg)

    def ews_Get_Bonjour_serviceName(self):
        """
        Disabling P9100 in the printer

        """
        try:
            print 'setting the Bonjour Service name'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            bonjourservicename=self.adapter.ews_get_text("Bonjour_Service_Name")
            self.adapter.ews_close_browser()
            return bonjourservicename

        except Exception, msg:
            raise AssertionError("Unable to Enable LPD -> %s" % msg)

    def ews_set_highestPrioirty(self,highestPriority):
        try:
            service_dict = {'1':'P9100', '2':'IPP', '3':'LPD'}
            print 'setting the highest Priority'
            self.adapter.ews_open_browser()
            self.adapter.ews_navigate_to_page("Bonjour", "https")
            self.adapter.ews_dropdown_select_by_text("Bonjour_Highest_Priority_Service",service_dict[highestPriority])
            self.adapter.ews_click_button("Apply")
            self.adapter.ews_close_browser()


        except Exception, msg:
            raise AssertionError("Unable to Enable LPD -> %s" % msg)
