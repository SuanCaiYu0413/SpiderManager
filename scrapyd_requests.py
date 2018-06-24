import requests
from scrapyd_api import ScrapydAPI


def connect_host(ip_address, port_num, timeout):
    url = 'http://' + ip_address + ':' + port_num + '/daemonstatus.json'
    try:
        req = requests.get(url, timeout=timeout).json()
    except Exception as e:
        req = {}
    return req


def scrapyd_connerct(ip_address, port_num):
    url = 'http://' + ip_address + ':' + port_num
    scrapyd = ScrapydAPI(url)
    return scrapyd
