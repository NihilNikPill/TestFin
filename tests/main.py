import xml.etree.ElementTree as ET
from xml import etree
import urllib.request
import datetime

def get_XML():
    url = f'http://www.cbr.ru/scripts/XML_daily.asp'
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    return root

def get_Code():
    url = 'https://www.cbr.ru/scripts/XML_valFull.asp'
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    l = list()
    for child in root:
        l.append(child.attrib)
    return l

root = get_XML()
for child in root:
    print(child.tag, child.attrib)
    for elem in child:
        print(elem.tag, elem.text)