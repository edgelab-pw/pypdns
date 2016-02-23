from pydns import *
import configparser

config = configparser.ConfigParser()
config['Server'] = {}
default = config['Server']
default['url'] = 'http://XXX.XXX.XXXX.XXX:8081/api/v1'
default['api_key'] = 'xxxx'

config.read('test.ini')

pydns = PyPDNSAPI(config['Server'].get('url'), config['Server'].get('api_key'))

payload = {
    "rrsets": [
        {
            "name": "hola.example.net",
            "type": "TXT",
            "changetype": "REPLACE",
            "records": [
                {
                    "content": '"Hello world"',
                    "disabled": False,
                    "name": "hola.example.net",
                    "ttl": 3600,
                    "type": "TXT",
                    "priority": 0
                }
            ]
        }
    ]
}

print(pydns.servers())
print(pydns.zones('localhost'))
print(pydns.zone('localhost', 'maillab.net'))
