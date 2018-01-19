import urllib.request
import json

BALANCE = 'http://www.flightradar24.com/balance.json'
AIRPORTS = 'http://www.flightradar24.com/_json/airports.php'
AIRLINES = 'http://www.flightradar24.com/_json/airlines.php'
ZONES = 'http://www.flightradar24.com/js/zones.js.php'

def get_server_balanced():
    template = urllib.request.urlopen(BALANCE).read().decode()
    B_data = json.loads(template)
    return min(B_data)


def get_airports():
    template = urllib.request.urlopen(AIRPORTS).read().decode()
    AP_data = json.loads(template)
    for i in AP_data['rows']:
        print(i)

def get_airlines():
    template = urllib.request.urlopen(AIRLINES).read().decode()
    AR_data = json.loads(template)
    for i in AR_data['rows']:
        print(i)

def get_zones():
    template = urllib.request.urlopen(ZONES).read().decode()
    Z_data = json.loads(template)
    for i in Z_data.keys():
        print(i + ' ' + str(Z_data[i]))

if __name__ == '__main__':
    get_server_balanced()