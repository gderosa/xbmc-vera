import httplib
import json

HTTP_PORT           = 3480
HTTP_TIMEOUT        = 70

# Must be smaller than HTTP_TIMEOUT, see:
# http://wiki.micasaverde.com/index.php/UI_Simple#lu_sdata:_The_polling_loop
POLLING_TIMEOUT     = 60

# Avoid flooding the network in case of lots of changes
MINIMUM_DELAY_MSECS = 300

class Controller:

    def __init__(self, host):
        self.host                   = host
        self.port                   = HTTP_PORT
        self.data                   = None

    # This method hangs for up to POLLING_TIMEOUT seconds if no changes,
    # so you won't need to time.sleep()
    def update(self):
        if self.data:
            # http://wiki.micasaverde.com/index.php/UI_Simple#lu_sdata:_The_polling_loop
            loadtime, dataversion = self.data['loadtime'], self.data['dataversion']
            query_string = \
'id=sdata&loadtime=%d&dataversion=%d&timeout=%d&minimumdelay=%d' % \
(loadtime, dataversion, POLLING_TIMEOUT, MINIMUM_DELAY_MSECS)
            # must be "killable" by parent thread via .sock.shutdown(...)
            self.updateConnection = httplib.HTTPConnection( \
                        self.host, self.port, timeout=HTTP_TIMEOUT )  
            self.updateConnection.request('GET', '/data_request?%s' % query_string)
            response = self.updateConnection.getresponse()
            update_data = json.load(response)
            if int(update_data['full']):
                self.data = update_data
            else:
                self.mergeData(update_data)
        else:
            self.getData()

    # Merges devices and scenes 
    def mergeData(self, update_data):
        # loadtime shouldn't need to be updated
        for k in ('loadtime', 'dataversion', 'state', 'comment'):
            if k in update_data.keys():
                self.data[k] = update_data[k]
        # TODO? a more efficient way? 
        for k in ('scenes', 'devices'):
            if k in update_data.keys():
                for updated in update_data[k]:
                    for i, device_or_scene in enumerate(self.data[k]):
                        if \
int(device_or_scene['id']) == int(updated['id']): 
                            self.data[k][i].update(updated)

    def getData(self):
        http = httplib.HTTPConnection(self.host, self.port, timeout=5)
        http.request('GET', '/data_request?id=sdata')
        response = http.getresponse() # it's an IO-like object
        self.data = json.load(response)

    # Tipically used to perform actions
    def GET(self, full_path, timeout=3):
        http = httplib.HTTPConnection(self.host, self.port, timeout=timeout)
        http.request('GET', full_path)
        response = http.getresponse()
        return response.read()


    



