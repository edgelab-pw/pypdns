from pydns.backend import *


class PyPDNSAPI(object):
    def __init__(self, host, apikey):
        self._store = {
            "backend": PyPdnsResourceAPI(host, apikey),
        }

    def servers(self):
        return self._store["backend"].servers.get()

    def zones(self, server):
        return self._store["backend"].servers(server).zones.get()

    def zone(self, server, zone):
        return self._store["backend"].servers(server).zones(zone).get()

    def create(self, server, zone, data):
        return self._store["backend"].servers(server).zones(zone).post(data)
