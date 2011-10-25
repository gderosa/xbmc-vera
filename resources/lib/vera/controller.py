import httplib
import json

HTTP_PORT           = 3480
HTTP_TIMEOUT        = 6

# Must be smaller than HTTP_TIMEOUT, see:
# http://wiki.micasaverde.com/index.php/UI_Simple#lu_sdata:_The_polling_loop
POLLING_TIMEOUT     = HTTP_TIMEOUT - 3

class Controller:

    def __init__(self, host):
        self.host = host
        self.port = HTTP_PORT
        self.data = None

    # This method hangs for up to POLLING_TIMEOUT seconds if no changes,
    # so you won't need to time.sleep()
    def update(self):
        if not self.data:
            self.getData()

        # http://wiki.micasaverde.com/index.php/UI_Simple#lu_sdata:_The_polling_loop
        loadtime, dataversion = self.data['loadtime'], self.data['dataversion']
        query_string = \
                'id=sdata&loadtime=%d&dataversion=%d&timeout=%d' % \
                (loadtime, dataversion, POLLING_TIMEOUT)

        http = httplib.HTTPConnection(self.host, self.port, timeout=HTTP_TIMEOUT) 
        http.request('GET', '/data_request?%s' % query_string)
        response = http.getresponse()
        update_data = json.load(response)

        self.mergeData(update_data) 

    # Only merges devices, currently (TODO) 
    def mergeData(self, update_data):
        # loadtime shouldn't need to be updated
        for k in ('dataversion', 'state', 'comment'):
            if k in update_data.keys():
                self.data[k] = update_data[k]
        # TODO? a more efficient way? 
        if 'devices' in update_data.keys():
            for updated_device in update_data['devices']:
                for i, device in enumerate(self.data['devices']):
                    if int(device['id']) == int(updated_device['id']): 
                        self.data['devices'][i].update(updated_device)

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


    



