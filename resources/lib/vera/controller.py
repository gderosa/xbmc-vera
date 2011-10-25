import httplib
import json

import time # DEBUG

class Controller:

    PORT = 3480

    def __init__(self, host):
        self.host = host
        self.port = Controller.PORT

    def update(self):
        print('vera.Controller.update()')
        time.sleep(5) 

    def getData(self):
        http = httplib.HTTPConnection(self.host, self.port)
        http.request('GET', '/data_request?id=sdata')
        response = http.getresponse() # it's an IO-like object
        self.data = json.load(response)

    def GET(self, full_path):
        http = httplib.HTTPConnection(self.host, self.port)
        http.request('GET', full_path)
        response = http.getresponse()
        return response.read()


    



