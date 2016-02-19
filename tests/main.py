from pydns import *
import configparser

config = configparser.ConfigParser()
config['Server'] = {}
default = config['Server']
default['url'] = 'http://XXX.XXX.XXXX.XXX:8081/api/v1'
default['api_key'] = 'xxxx'

config.read('test.ini')

pydns = PyPdnsAPI(config['Server'].get('url'),config['Server'].get('api_key'))

print(pydns.servers.get())
print(pydns.servers.localhost.zones.get())

