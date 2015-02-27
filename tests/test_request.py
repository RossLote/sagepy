from pysagepay.request import Request
from pysagepay.response import Response, FakeResponse
from pysagepay.utils import encode_transaction_request
from unittest import TestCase
from nose.tools import *
import mock

class TestRequest(TestCase):
    def test_set_url(self):
        request = Request()
        url = 'https://test.com'
        request.set_url(url)
        self.assertEqual(request._url, url)
        url = 'http://test.com'
        self.assertRaises(ValueError, request.set_url, url)
        
    def test_set_payload(self):
        r = Request()
        d = {'test' : 'tester', 'again': 400}
        dd = encode_transaction_request(d)
        r.set_payload(d)
        self.assertEqual(dd, r._payload)
    
    @mock.patch('urllib2.urlopen')
    def test_send(self, mock_obj):
        mock_obj.side_effect = [FakeResponse("hello=test\r\nfoo=bar\r\n")]
        request = Request(url='https://test.com', payload={})
        r = request.send()
        ok_(isinstance(r, Response))
        self.assertDictEqual({'hello':'test','foo':'bar'}, r._response)