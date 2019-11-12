import lxml.etree as et
import time

class SoapXmlUtilities:
    #packet_received = ''
    def __init__(self):
        pass

    #   ===================== Modify payload values ============================================== #
    def modify_tag_values(self, xml_file, tags_to_modify):
        """
        Modify the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2     |
        | xml file     | tags to modify |

        """
        try:
            tree = et.fromstring(xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "CancelScanJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetScannerElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetScanJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005",
                             "wsd": "http://schemas.xmlsoap.org/ws/2005/04/discovery",
                             "ddxmlns": "http://www.hp.com/schemas/imaging/con/dictionaries/1.0"
                             }
            for tag in tags_to_modify:
                tag_name = tag[0]
                new_tag_value = tag[1]
                tree.find ('.//' + tag_name, namespaces=xml_namespace).text = new_tag_value
            return et.tostring (tree)
        except:
            raise AssertionError('Unable to modify tags')

    #   ===================== Modify payload values ============================================== #
    def modify_tag_values_scan(self, xml_file, tags_to_modify):
        """
        Modify the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2     |
        | xml file     | tags to modify |

        """
        try:
            tree = et.fromstring (xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "RetrieveImageRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005"}
            for tag in tags_to_modify:
                tag_name = tag[0]
                new_tag_value = tag[1]
                tree.find ('.//' + tag_name, namespaces=xml_namespace).text = new_tag_value

            return et.tostring (tree)
        except:
            raise AssertionError ('Unable to modify tags')

    #   ===================== Delete specific tag from payload  ============================================== #
    def delete_tag(self, xml_file, tag_to_remove):
        """
        Delete the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2     |
        | xml file     | tags to delete |

        """
        try:
            tree = et.fromstring(xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "CancelScanJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetScanJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005"}
            tag_node = tree.findall('.//' + tag_to_remove, namespaces=xml_namespace)
            for tag in tag_node:
                tag.getparent().remove(tag)
            return et.tostring(tree)
        except:
            raise AssertionError('Unable to delete tags')

            #   =================== Reading tag values ================================================ #

    #  ===================== Reading payload values ============================================== #
    def get_tag_values(self, data, tag_name):
        """
        Reading the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2  |
        | data         | tag name    |

        """
        try:
            tree = et.fromstring(data)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                   "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                   "SOAP-ENV": "http://www.w3.org/2003/05/soap-envelope",
                   "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                   "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                   "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing"}
            tag_value = tree.find('.//' + tag_name, namespaces=xml_namespace).text
            return tag_value
        except:
            raise AssertionError('unable to retrieve tag values')

    #   ===================== Reading  payload values ============================================== #

    # =================== Adding tag  ================================================ #
    def add_tag(self, xml_file, previous_tag, new_tag_name, tag_text, tag_prefix):
        """
        Adding the payload tag values dynamically at run time

        Arguments: The keyword takes 5 arguments.
        | Argument 1   | Argument 2    | Argument 3   | Argument 4  | Argument 5  |
        | xml file     | previous tag  | New tagname  | tag text    | tag prefix  |

        """
        try:
            tree = et.fromstring(xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005"}
            tag_value = tree.find('.//' + previous_tag, namespaces=xml_namespace)
            if tag_prefix != '':
                sub_tag = et.Element(et.QName((xml_namespace.get(tag_prefix)), new_tag_name))
            else:
                sub_tag = et.Element(new_tag_name)
            sub_tag.text = tag_text
            tag_value.addnext(sub_tag)
            return et.tostring(tree)
        except:
            raise AssertionError('unable to Add tag and its tag value')

    def replace_tag_name(self, xml_file, existing_tag, new_tag):
        """
        Modify the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2     |
        | xml file     | tags to modify |

        """
        try:
            tree = et.fromstring(xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "CancelScanJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005"}
            locate_tag = tree.find('.//' + existing_tag, namespaces=xml_namespace)
            locate_tag.tag = new_tag
            return et.tostring(tree)
        except:
            raise AssertionError('Unable to modify tags')

    def set_tag_attributes(self, xml_file, tag_name, attribute_name, attribute_value):
        """
        set the payload tag values dynamically at run time

        Arguments: The keyword takes 2 arguments.
        | Argument 1   | Argument 2  |
        | data         | tag name    |

        """
        try:
            time.sleep(3)
            tree = et.fromstring(xml_file)
            xml_namespace = {"wprt": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wsa": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "soap-env": "http://www.w3.org/2003/05/soap-envelope",
                             "xmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "CancelJobRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "Fromxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "Subscribexmlns": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "Addressxmlns": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                             "GetPrinterElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "GetJobElementsRequestxmlns": "http://schemas.microsoft.com/windows/2006/08/wdp/print",
                             "wse": "http://schemas.xmlsoap.org/ws/2004/08/eventing",
                             "DeliveryMode": "http://schemas.xmlsoap.org/ws/2004/08/eventing/DeliveryModes/Push",
                             "wscn": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "sca": "http://schemas.microsoft.com/windows/2006/08/wdp/scan",
                             "UNS1xmlns": "http://www.microsoft.com/windows/test/testdevice/11/2005"}
            tag_value = tree.find('.//' + tag_name, namespaces=xml_namespace)
            tag_value.set(attribute_name, attribute_value)
            return et.tostring(tree)
        except:
            raise AssertionError('unable to set tag values')