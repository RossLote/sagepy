import urllib2
from utils import encode_transaction_request
from .response import Response

class Request(object):
    def __init__(self, url='https://none', payload={}):
        self.set_url(url)
        self.set_payload(payload)
        
    def send(self):
        request = urllib2.Request(self._url, self._payload)
        try:
            response = urllib2.urlopen(request)
            return Response(response, self._payload)
        except urllib2.URLError:
            return Response.get_network_error_response(self._payload)
        
    def set_url(self, url):
        if not url.startswith('https://'):
            raise ValueError('url must begin with https://')
        self._url = url
        
    def set_payload(self, payload):
        self._payload = encode_transaction_request(payload)