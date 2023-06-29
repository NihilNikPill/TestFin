from main import get_XML, get_Code
from lxml import etree 
import urllib.request
import urllib.parse
import requests
import datetime

money = get_XML()
codes = get_Code()

def test_xml_validity():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    xml_data = response.content
    
    xsd_url = "http://www.cbr.ru/StaticHtml/File/92172/ValCurs.xsd"
    xsd_response = requests.get(xsd_url)
    xsd_data = xsd_response.content

    schema = etree.XMLSchema(etree.fromstring(xsd_data))
    parser = etree.XMLParser(schema=schema)

    try:
        etree.fromstring(xml_data, parser)
        assert True
    except etree.XMLSyntaxError:
        assert False, "XML-файл не проходит проверку по заданной XSD-схеме"


def test_tags():
    elem_tag = ['NumCode', 'CharCode', 'Nominal', 'Name', 'Value']
    for child in money:
        if child.tag == 'Valute':
            i = 0
            for elem in child:
                if elem.tag == elem_tag[i]:
                    i += 1
                else:
                    assert False
        else:
            assert False
    assert True

def test_nums():
    for child in money:
        if child.attrib not in codes:
            assert False
        for elem in child:
            if elem.tag != 'NumCode' and elem.tag != 'Nominal' and elem.tag != 'Value':
                if not type(elem.tag).istitle:
                    assert False
            else:
                if not type(elem.text).isdigit:
                    assert False        
    assert True

def test_date_format():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    xml_data = response.text

    root = etree.fromstring(bytes(xml_data, encoding = ('Windows-1251')))
    date = root.attrib["Date"]

    expected_format = "%d.%m.%Y" 

    try:
        datetime.datetime.strptime(date, expected_format)
    except ValueError:
        assert False

def test_content_type():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    
    expected_content_type = "application/xml; charset=windows-1251"
    
    assert response.headers["Content-Type"] == expected_content_type, f"Неверный тип контента. Ожидаемый тип: {expected_content_type}, Фактический тип: {response.headers['Content-Type']}"     
    
def test_exception_handling():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = response.text
    
        etree.fromstring(bytes(xml_data, encoding = ('Windows-1251')))
        assert True
    except (requests.exceptions.RequestException, etree.ParseError):
        assert False, "Исключение было вызвано"

