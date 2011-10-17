import httplib
import json

class Controller:

    PORT = 3480

    def __init__( self, host ):
        self.host = host
        self.port = Controller.PORT

    def getData( self ):
        http = httplib.HTTPConnection(self.host, self.port)
        http.request('GET', '/data_request?id=sdata')
        response = http.getresponse() # it's an IO-like object
        self.data = json.load(response)

    



